import logging
from dataclasses import dataclass
from typing import Any, Dict

import ase
import ase.io as aio
import numpy as np
from pydantic import BaseModel
from ray import serve
from ray.serve import Application
from starlette.requests import Request
from zndraw.data import atoms_from_json, atoms_to_json
from fastapi import FastAPI

from simgen.atoms_cleanup import attach_calculator, relax_hydrogens, run_dynamics
from simgen.calculators import MaceSimilarityCalculator
from simgen.element_swapping import SwappingAtomicNumberTable
from simgen.generation_utils import calculate_restorative_force_strength
from simgen.hydrogenation import NATURAL_VALENCES, add_hydrogens_to_atoms
from simgen.integrators import IntegrationParameters
from simgen.manifolds import PointCloudPrior
from simgen.particle_filtering import ParticleFilterGenerator
from simgen.utils import (
    get_hydromace_calculator,
    get_mace_config,
    get_mace_similarity_calculator,
    get_system_torch_device_str,
    setup_logger,
    time_function,
)

INTEGRATION_PARAMS = IntegrationParameters(S_churn=1.3, S_min=2e-3, S_noise=0.5)
swapping_z_table = SwappingAtomicNumberTable([6, 7, 8], [1, 1, 1])

setup_logger(level=logging.INFO)

app = FastAPI()

@dataclass
class CommonData:
    atom_ids: list[int]
    atoms: ase.Atoms
    points: np.ndarray
    segments: np.ndarray


class RequestStructure(BaseModel):
    run_type: str
    run_specific_params: Dict[str, Any]
    common_data: Dict[str, Any]


def format_common_data(data: dict):
    atom_ids = data["atom_ids"]
    atoms = atoms_from_json(data["atoms"])
    points = data["points"]
    if points is None:
        points = [[0.0, 0.0, 0.0]]
    points = np.array(points)
    segments = np.array(data["segments"])
    formated_data = CommonData(
        atom_ids=atom_ids, atoms=atoms, points=points, segments=segments
    )
    return formated_data


def _jsonify_atoms(*args: ase.Atoms) -> dict:
    atoms = [atoms_to_json(x) for x in args]
    return {"atoms": atoms}


def parse_request(data: dict):
    try:
        parsed_data = RequestStructure.parse_obj(data)
        return parsed_data
    except Exception as e:
        logging.error("Couldn't parse the request to the inference serve")
        raise e
    
def hydrogenate_by_bond_lengths(atoms, graph_representation):
    edge_array = nx.adjacency_matrix(graph_representation).todense()  # type: ignore
    current_neighbours = edge_array.sum(axis=0)
    max_valence = np.array(
        [
            NATURAL_VALENCES[atomic_number]
            for atomic_number in atoms.get_atomic_numbers()
        ]
    )
    num_hs_to_add_per_atom = max_valence - current_neighbours
    atoms_with_hs = add_hydrogens_to_atoms(atoms, num_hs_to_add_per_atom)
    return atoms_with_hs


def hydrogenate_by_model(atoms, model):
    num_hs_to_add_per_atom = model.predict_missing_hydrogens(atoms)
    num_hs_to_add_per_atom = np.round(num_hs_to_add_per_atom).astype(int)
    atoms_with_hs = add_hydrogens_to_atoms(atoms, num_hs_to_add_per_atom)
    return atoms_with_hs


@serve.deployment(
    ray_actor_options={"num_gpus": 1, "num_cpus": 16},
    autoscaling_config={"min_replicas": 0, "max_replicas": 1},
)
@serve.ingress(app)
class GenerationServer:
    def __init__(
        self,
        mace_models_path,
        device="cpu",
    ) -> None:
        self.moldiff_calc = get_mace_similarity_calculator(
            mace_models_path, num_reference_mols=-1, device=device
        )
        self.hydromace_calc = get_hydromace_calculator(mace_models_path, device=device)
        self.device = device

    @app.post("/")
    async def run(self, request: Request) -> dict:
        raw_data = await request.json()
        run_schema = parse_request(raw_data)
        common_data = format_common_data(run_schema.common_data)
        run_type = run_schema.run_type.strip().lower()
        run_specific_params = run_schema.run_specific_params
        if run_type == "generate":
            return self.generate(run_specific_params, common_data)
        elif run_type == "hydrogenate":
            return self.hydrogenate(run_specific_params, common_data)
        elif run_type == "relax":
            return self.relax(run_specific_params, common_data)
        elif run_type == "get_mace_config":
            return self.get_model_config()
        else:
            logging.error(
                f"Encountered unsupported `run_type`: {run_type}. Returning original atoms"
            )
            return atoms_to_json(common_data.atoms)

    def generate(self, run_params: dict, common_data: CommonData) -> dict:
        moldiff_calc = self.moldiff_calc
        points = common_data.points
        atoms = common_data.atoms
        prior = PointCloudPrior(points, beta=5.0)
        num_atoms_to_add = run_params["num_atoms_to_add"]
        restorative_force_multiplier = run_params["restorative_force_multiplier"]
        restorative_force_strength = (
            calculate_restorative_force_strength(num_atoms_to_add)
            * restorative_force_multiplier
        )

        generator = ParticleFilterGenerator(
            moldiff_calc,
            prior,
            integration_parameters=INTEGRATION_PARAMS,
            device=self.device,
            restorative_force_strength=restorative_force_strength,
        )

        mol = ase.Atoms(f"C{num_atoms_to_add}")
        mol = prior.initialise_positions(mol, scale=0.5)
        molecule, mask, torch_mask = generator._merge_scaffold_and_create_mask(
            mol, atoms, num_particles=10, device=self.device
        )
        logging.info(f"Running main generation loop on device {self.device}")
        with time_function("Main generation loop") as _:
            trajectories = generator._maximise_log_similarity(
                molecule,
                particle_swap_frequency=4,
                num_particles=10,
                swapping_z_table=swapping_z_table,
                mask=mask,
                torch_mask=torch_mask,
            )
        logging.info("You can now add hydrogens and relax the structure.")
        return _jsonify_atoms(*trajectories)

    def relax(self, run_params: dict, common_data: CommonData) -> dict:
        atom_ids = common_data.atom_ids
        atoms = common_data.atoms
        if len(atom_ids) != 0:
            logging.info("Will relax only the selected atoms")
            mask = np.ones(len(atoms)).astype(bool)
            mask[atom_ids] = False
        else:
            logging.info("Will relax all atoms")
            mask = np.zeros(len(atoms)).astype(bool)
        relaxed_atoms = attach_calculator(
            [atoms], self.moldiff_calc, calculation_type="mace", mask=mask
        )
        logging.info("Relaxing structure")
        relaxed_atoms = run_dynamics(relaxed_atoms, num_steps=run_params["max_steps"])
        logging.info("Finished relaxation")
        return _jsonify_atoms(*relaxed_atoms)

    def hydrogenate(self, run_params: dict, common_data: CommonData) -> dict:
        moldiff_calc = self.moldiff_calc
        hydromace_calc = self.hydromace_calc
        atoms = common_data.atoms
        max_steps = run_params["max_steps"]
        if hydromace_calc is None:
            logging.info(
                "Couldn't load a hydromace model. Will hydrogenate by bond lengths"
            )
            return self._hydrogenate_by_bond_lengths(atoms, moldiff_calc, max_steps)
        else:
            logging.info("Found a hydromace model. Will use it to hydrogenate.")
            return self._hydrogenate_by_model(
                atoms, hydromace_calc, moldiff_calc, max_steps
            )
    @app.get("/config")
    def get_model_config(
        self
        # , request: Request
    ) -> dict:
        return get_mace_config(self.moldiff_calc.model)

    def _hydrogenate_by_bond_lengths(self, atoms, moldiff_calc, max_steps: int) -> dict:
        connectivity_graph, found, error = self._try_to_get_graph_representation(atoms)
        if not found:
            logging.info(
                "No graph representation found, try resetting the scene or clicking `Save` in the `Bonds` tab"
            )
            logging.info(f"Error: {error}")
            return _jsonify_atoms(atoms)
        else:
            hydrogenated_atoms = hydrogenate_by_bond_lengths(atoms, connectivity_graph)
            logging.info("Hydrogens added, now running relaxation.")
            relaxed = self._relax_hydrogenated_structure(
                hydrogenated_atoms, moldiff_calc, num_steps=max_steps
            )
            logging.info("Done")
            return _jsonify_atoms(hydrogenated_atoms, relaxed)

    def _hydrogenate_by_model(
        self, atoms, hydromace_calc, moldiff_calc, max_steps: int
    ) -> dict:
        hydrogenated_atoms = hydrogenate_by_model(atoms, hydromace_calc)
        logging.info("Hydrogens added, now running relaxation.")
        relaxed = self._relax_hydrogenated_structure(
            hydrogenated_atoms, moldiff_calc, num_steps=max_steps
        )
        logging.info("Done")
        return _jsonify_atoms(hydrogenated_atoms, relaxed)

    @staticmethod
    def _relax_hydrogenated_structure(atoms, calc, num_steps) -> ase.Atoms:
        to_relax = atoms.copy()
        relaxed = relax_hydrogens([to_relax], calc, num_steps=num_steps, max_step=0.1)[
            0
        ]
        return relaxed

    @staticmethod
    def _try_to_get_graph_representation(atoms):
        try:
            connectivity_graph = atoms.info["graph_representation"]
            found = True
            error = None
        except Exception as e:
            connectivity_graph = None
            found = False
            error = e
        return connectivity_graph, found, error
 
from typing import Iterable
import ase
from itertools import zip_longest
import numpy as np

"""
Tools for relaxing many small molecules in a batched way using a MACE model.
"""


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def create_relaxation_batches(
    atoms: Iterable[ase.Atoms], batch_size=32, separation_distance=100.0
):
    batches = []
    atoms_copy = [x.copy() for x in atoms]
    for batch_atoms in grouper(atoms_copy, batch_size):
        batch_atoms: list[ase.Atoms] = [a for a in batch_atoms if a is not None]
        batched_atoms = ase.Atoms()
        batch_index = []
        previous_largest_x = 0
        for i, at in enumerate(batch_atoms):
            batch_index.extend([i] * len(at))
            min_x = at.get_positions()[:,0].min()
            at.set_positions(
                at.get_positions()
                + (previous_largest_x + separation_distance - min_x)
                * np.array([[1.0, 0.0, 0.0]])
            )
            previous_largest_x = at.get_positions()[:,0].max()
            batched_atoms += at
        batched_atoms.arrays["batch_index"] = np.array(batch_index)
        batches.append(batched_atoms)
    return batches


def split_relaxation_batch(batch: ase.Atoms) -> list[ase.Atoms]:
    """
    Split a batch of atoms into individual molecules using the batch_index array.
    """
    molecules = []
    unique_indices = np.unique(batch.arrays["batch_index"])
    for index in unique_indices:
        mask = batch.arrays["batch_index"] == index
        molecule = batch[mask]
        molecule.positions -= molecule.positions.mean(axis=0)
        molecules.append(molecule)
    return molecules

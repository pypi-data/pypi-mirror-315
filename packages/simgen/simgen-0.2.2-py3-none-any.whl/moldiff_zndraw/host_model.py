import dask
import numpy as np
from distributed import Client, LocalCluster
from hydromace.interface import HydroMaceCalculator

from simgen.calculators import MaceSimilarityCalculator
from simgen.utils import (
    get_hydromace_calculator,
    get_mace_similarity_calculator,
)


@dask.delayed
def get_mace_model(
    model_repo_path: str, device: str = "cpu"
) -> MaceSimilarityCalculator:
    # Load the actual pytorch model, done only once.
    rng = np.random.default_rng(0)
    score_model = get_mace_similarity_calculator(
        model_repo_path,
        num_reference_mols=-1,
        device=device,
        rng=rng,
    )
    return score_model


@dask.delayed
def get_hydromace_model(
    model_repo_path: str, device: str = "cpu"
) -> HydroMaceCalculator | None:
    hydromace_calc = get_hydromace_calculator(model_repo_path, device)
    return hydromace_calc


def launch_local_cluster(model_repo_path: str, device: str) -> Client:
    print("Launching a local cluster at port 31415")
    cluster = LocalCluster(scheduler_port=31415, n_workers=1, memory_limit=None)
    client = Client("tcp://127.0.0.1:31415")
    model = get_mace_model(model_repo_path, device).persist()
    hydromace_model = get_hydromace_model(model_repo_path, device).persist()
    client.publish_dataset(model=model, hydromace_model=hydromace_model)
    print("Loaded the following:")
    print(client.list_datasets())
    return client


def get_loaded_client(model_repo_path: str, device: str):
    try:
        client = Client("tcp://127.0.0.1:31415", timeout=5)  # type:ignore
        return client
    except OSError:
        print("Couldn't connect to already running client\nLaunching a local cluster")
        client = launch_local_cluster(model_repo_path=model_repo_path, device=device)
        return client
    except Exception as e:
        print("Something went horribly wrong")
        raise e

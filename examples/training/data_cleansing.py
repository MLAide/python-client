import pandas as pd

from mlaide.model import ArtifactRef
from mlaide.client import MvcClient

from parameters import get_project_key, get_experiment_key


def run_cleansing(project_key: str, experiment_key: str):
    # create mvc client
    mvc_client = MvcClient(project_key=project_key)

    ##################
    # Create a new run
    # Also attach the input artifacts to this run
    artifact_ref = ArtifactRef(name="wine quality red raw data", version=1)
    run = mvc_client.start_new_run(experiment_key=experiment_key,
                                   run_name="data cleansing",
                                   used_artifacts=[artifact_ref])

    # Read the wine-quality csv file and do some "cleansing"
    df = pd.read_csv("./winequality-red.csv", sep=";")
    df = df.iloc[::2, :]  # only take each second row...
    df.to_csv("./cleaned.csv", sep=";")

    ###############################
    # Attach the dataset to the run
    metadata = {
        "description": "removed each second row"
    }
    artifact = run.create_artifact(name="wine quality red cleaned", artifact_type="dataset", metadata=metadata)
    run.add_artifact_file(artifact, './cleaned.csv')
    run.add_artifact_file(artifact, './sub/data.txt')

    ##########################
    # Set the run as completed
    run.set_completed_status()


if __name__ == "__main__":
    p = get_project_key()
    e = get_experiment_key()
    run_cleansing(p, e)

import os
import pandas as pd

from modelversioncontrol.artifact_ref import ArtifactRef
from modelversioncontrol.artifact import Artifact
from modelversioncontrol.client import MvcClient

project_key = os.getenv("MVC_PROJECT_KEY")
experiment_key = os.getenv("MVC_EXPERIMENT_KEY", None)

if project_key is None:
    project_key = input("Enter project key: ")
if experiment_key is None:
    experiment_key = input("Enter experiment key: ")

# create mvc client
mvc_client = MvcClient()


if __name__ == "__main__":
    ##################
    # Create a new run
    # Also attach the input artifacts to this run
    artifact_ref = ArtifactRef(name="wine quality red raw data", version=1)
    run = mvc_client.start_new_run(project_key=project_key,
                                   experiment_key=experiment_key,
                                   run_name="data cleansing",
                                   used_artifacts=[artifact_ref])

    # Read the wine-quality csv file and do some "cleansing"
    df = pd.read_csv("./winequality-red.csv", sep=";")
    df = df.iloc[::2, :]  # only take each second row...
    df.to_csv("./cleaned.csv", sep=";")

    ###############################
    # Attach the dataset to the run
    artifact = Artifact(name="wine quality red cleaned", type="dataset")
    artifact.add_file('./cleaned.csv')
    artifact.metadata = {
        "description": "removed each second row"
    }
    run.log_artifact(artifact)

    ##########################
    # Set the run as completed
    run.set_completed_status()

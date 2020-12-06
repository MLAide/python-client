import os
import shutil
import urllib.request

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
    run = mvc_client.start_new_run(project_key=project_key,
                                   experiment_key=experiment_key,
                                   run_name="data ingest")

    # Read the wine-quality csv file from the URL and store on local filesystem
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    with urllib.request.urlopen(csv_url) as response, open("./winequality-red.csv", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    ###############################
    # Attach the dataset to the run
    artifact = Artifact(name="wine quality red raw data", type="dataset")
    artifact.add_file('./winequality-red.csv')
    artifact.metadata = {
        "source": csv_url
    }
    run.log_artifact(artifact)

    ##########################
    # Set the run as completed
    run.set_completed_status()

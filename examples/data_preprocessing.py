import os
import shutil
import urllib.request

from modelversioncontrol.artifact import Artifact
from modelversioncontrol.client import MvcClient

experiment_key = os.getenv("MVC_EXPERIMENT_KEY", None)
mvc_client = MvcClient()


if __name__ == "__main__":
    ##################
    # Create a new run
    run = mvc_client.start_new_run(project_key="projekt",
                                   experiment_key=experiment_key,
                                   run_name="wine-quality-data-preprocessing")

    # Read the wine-quality csv file from the URL and store on local filesystem
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    with urllib.request.urlopen(csv_url) as response, open("./winequality-red.csv", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    ###############################
    # Attach the dataset to the run
    artifact = Artifact(name="winequality-red.csv", type="dataset")
    artifact.add_file('./winequality-red.csv')
    artifact.metadata = {
        "source": csv_url
    }
    run.log_artifact(artifact)

    ##########################
    # Set the run as completed
    run.set_completed_status()

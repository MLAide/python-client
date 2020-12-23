import shutil
import urllib.request

from modelversioncontrol.client import MvcClient
from parameters import get_project_key, get_experiment_key


def run_ingest(project_key: str, experiment_key: str):
    # create mvc client
    mvc_client = MvcClient()

    ##################
    # Create a new run
    run = mvc_client.start_new_run(project_key=project_key,
                                   experiment_key=experiment_key,
                                   run_name="data ingest")

    # Read the wine-quality csv file from the URL and store on local filesystem
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    with urllib.request.urlopen(csv_url) as response, open("./winequality-red.csv", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    ##############################################
    # Attach the dataset to the run as an artifact
    metadata = {
        "source": csv_url
    }
    artifact = run.create_artifact(name="wine quality red raw data", type="dataset", metadata=metadata)
    run.add_artifact_file(artifact, './winequality-red.csv')

    ##########################
    # Set the run as completed
    run.set_completed_status()


if __name__ == "__main__":
    p = get_project_key()
    e = get_experiment_key()
    run_ingest(p, e)

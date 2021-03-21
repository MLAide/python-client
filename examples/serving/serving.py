import cloudpickle
import numpy as np
from sklearn.linear_model import ElasticNet
from typing import Union

from mlaide.client import MLAideClient


def start_serving(project_key: str, artifact_name: str, artifact_version: Union[str, int]):
    # create mlaide client
    mlaide_client = MLAideClient(project_key=project_key)

    artifact = mlaide_client.get_artifact(artifact_name=artifact_name, artifact_version=artifact_version)

    artifact_bytes = artifact.load('model.pkl')
    artifact_bytes.seek(0)
    cls: ElasticNet = cloudpickle.load(artifact_bytes)

    # Alternatively the artifact can be downloaded and saved on disk. After that we can load the model from local fs
    # artifact.download('./model')
    # cls: ElasticNet = cloudpickle.load(open("./model/model.pkl", "rb"))

    n = np.array([[7.4, 0.7, 0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4]])
    print(cls.predict(n))


if __name__ == "__main__":
    start_serving('workflow', 'Elasticnet Wine Model', 24)

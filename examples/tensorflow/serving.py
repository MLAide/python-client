import tensorflow as tf
from typing import Union

from mlaide.client import MLAideClient


def start_serving(project_key: str, artifact_name: str, artifact_version: Union[str, int]):
    # create mlaide client
    mlaide_client = MLAideClient(project_key=project_key)

    artifact = mlaide_client.get_artifact(name=artifact_name, version=artifact_version)

    artifact.download('./model')
    my_model = tf.keras.models.load_model('./model')

    n = np.array([[7.4, 0.7, 0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4]])
    print(cls.predict(n))


if __name__ == "__main__":
    start_serving('workflow', 'Elasticnet Wine Model', 24)

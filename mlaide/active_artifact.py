from . import mapper, _model_deser
from ._api_client import Client
from ._api_client.api import artifact_api
from .model import Artifact, ModelStage

from dataclasses import replace
from io import BytesIO
from typing import Optional, Tuple
from zipfile import ZipFile


class ActiveArtifact(object):
    """This class provides access to artifacts that are stored in ML Aide"""

    __api_client: Client
    __project_key: str
    __artifact: Artifact
    __cached_zip: Tuple[BytesIO, Optional[str]] = None

    def __init__(self,
                 api_client: Client,
                 project_key: str,
                 artifact_name: str,
                 artifact_version: Optional[int],
                 model_stage: Optional[ModelStage] = None):
        self.__api_client = api_client
        self.__project_key = project_key
        self.__artifact = self.__load_artifact(artifact_name, artifact_version, model_stage)

    def __load_artifact(self, artifact_name: str, artifact_version: Optional[int],
                        model_stage: Optional[ModelStage]) -> Artifact:
        artifact_dto = artifact_api.get_artifact(client=self.__api_client,
                                                 project_key=self.__project_key,
                                                 artifact_name=artifact_name,
                                                 artifact_version=artifact_version,
                                                 model_stage=model_stage.value if model_stage is not None else None)
        return mapper.dto_to_artifact(artifact_dto)

    @property
    def artifact(self) -> Artifact:
        # Return a deep copy to avoid changing anything by the client
        return replace(self.__artifact)

    def load(self, filename: str) -> BytesIO:
        """Load a specific file of this artifact into memory

        Arguments:
            filename: The name of the file that should be loaded
        """

        # TODO: Do not download whole zip; instead download just the single file
        zip_bytes, zip_filename = self.__download_zip()
        with ZipFile(zip_bytes) as z:
            zip_info = z.infolist()
            desired_file = next(info for info in zip_info if info.filename == filename)
            with z.open(desired_file, 'r') as zip_file:
                return BytesIO(zip_file.read())

    def load_model(self):
        model_binary = self.load("model.pkl")
        return _model_deser.deserialize(model_binary)

    def download(self, target_directory: str):
        """Downloads all files of this artifact and stores them into the specified directory.

        Arguments:
            target_directory: The path to the directory where all files should be stored.
        """

        # download
        artifact_bytes, artifact_filename = self.__download_zip()

        # unzip and write to disk
        with ZipFile(artifact_bytes) as z:
            z.extractall(target_directory)

    def __download_zip(self) -> (BytesIO, str):
        if self.__cached_zip is None:
            self.__cached_zip = artifact_api.download_artifact(client=self.__api_client,
                                                               project_key=self.__project_key,
                                                               artifact_name=self.__artifact.name,
                                                               artifact_version=self.__artifact.version)

        return self.__cached_zip

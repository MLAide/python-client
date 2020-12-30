from . import mapper
from ._api_client import Client
from ._api_client.api import artifacts
from .model import Artifact

from dataclasses import replace
from io import BytesIO
from typing import Union
from zipfile import ZipFile


class ActiveArtifact(object):
    __api_client: Client
    __project_key: str
    __artifact: Artifact
    __cached_zip: BytesIO = None

    def __init__(self,
                 api_client: Client,
                 project_key: str,
                 artifact_name: str,
                 artifact_version: Union[str, int]):
        self.__api_client = api_client
        self.__project_key = project_key
        self.__artifact = self.__load_artifact(artifact_name, artifact_version)

    def __load_artifact(self, artifact_name: str, artifact_version: Union[str, int]) -> Artifact:
        artifact_dto = artifacts.get_artifact(client=self.__api_client,
                                              project_key=self.__project_key,
                                              artifact_name=artifact_name,
                                              artifact_version=artifact_version)
        return mapper.from_artifact_dto(artifact_dto)

    @property
    def artifact(self) -> Artifact:
        # Return a deep copy to avoid changing anything by the client
        return replace(self.__artifact)

    def load(self, filename: str) -> BytesIO:
        zip_bytes, zip_filename = self.__download_zip()
        with ZipFile(zip_bytes) as z:
            zip_info = z.infolist()
            desired_file = next(info for info in zip_info if info.filename == filename)
            with z.open(desired_file, 'r') as zip_file:
                return BytesIO(zip_file.read())

    def download(self, target_directory: str):
        # download
        artifact_bytes, filename = self.__download_zip()

        # unzip and write to disk
        with ZipFile(artifact_bytes) as z:
            z.extractall(target_directory)

    def __download_zip(self) -> (BytesIO, str):
        if self.__cached_zip is None:
            self.__cached_zip = artifacts.download_artifact(client=self.__api_client,
                                                            project_key=self.__project_key,
                                                            artifact_name=self.__artifact.name,
                                                            artifact_version=self.__artifact.version)

        return self.__cached_zip

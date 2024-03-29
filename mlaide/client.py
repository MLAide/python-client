from __future__ import annotations

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass

from mlaide.active_experiment import ActiveExperiment

from ._api_client import Client, AuthenticatedClient
from .active_artifact import ActiveArtifact
from .model import ModelStage


@dataclass
class ConnectionOptions:
    """Specify options for a MLAideClient"""

    server_url: Optional[str]
    api_key: Optional[str]

    def __init__(self, server_url: str = None, api_key: str = None):
        self.server_url = server_url
        self.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "server_url": self.server_url,
            "api_key": self.api_key
        }

        # Remove values from dict that are None
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ConnectionOptions:
        if d is None:
            d = dict()

        options = ConnectionOptions(
            server_url=d.get("server_url", None),
            api_key=d.get("api_key", None)
        )

        return options


class MLAideClient:
    """This is the main entry point to use this library. Creates a connection to the ML Aide server and provides
    read and write access to all resources.
    """

    __options: ConnectionOptions
    __api_client: Client
    __project_key: str

    def __init__(self, project_key: str, options: ConnectionOptions = None):
        """Creates a new instance of this class.

        Arguments:
            project_key: The key of the project, that should be accessed. All operations will be made on this project.
            options: Optional options that will be used to establish a connection.
        """
        if project_key is None:
            raise ValueError("project key must be not None")
        self.__project_key = project_key

        if options is None:
            self.__options = MLAideClient.__get_default_options()
        else:
            self.__options = MLAideClient.__merge_options(MLAideClient.__get_default_options(), options)

        self.__api_client = AuthenticatedClient(base_url=self.__options.server_url,
                                                api_key=self.__options.api_key)

    def create_experiment(self, experiment_name: str):
        return ActiveExperiment(api_client=self.__api_client, project_key=self.__project_key, experiment_name=experiment_name)

    def get_artifact(self, name: str, version: Optional[int] = None) -> ActiveArtifact:
        """Gets an existing artifact. The artifact is specified by its name and version. If no version
        is specified, the latest available version of the artifact will be used.

        Arguments:
            name: The name of the artifact.
            version: The (optional) version of the artifact. If no version is specified, the latest available version
                will be loaded.

        Returns:
             This object encapsulates an artifact and provides functions to interact with the artifact.
        """

        return ActiveArtifact(self.__api_client, self.__project_key, name, version)

    def load_model(self,
                   name: str,
                   version: Optional[int] = None,
                   stage: Optional[ModelStage] = None) -> any:
        """Loads and restores a model. The model is specified by its name and version. If no version
        is specified, the latest available version of the model will be used.

        Arguments:
            name: The name of the model.
            version: The (optional) version of the model. If no version is specified, the latest available version will
                be loaded.
            stage: This argument can only be used when version is None. In this case the latest model can be filtered by
                its stage. In reverse this means that all model versions will be ignored when they have not the
                specified stage.

        Returns:
             The model. E.g. in the case of a scikit-learn model the return value will be a deserialized model that
             can be used for predictions using `.predict(...)`.
         """

        if version is not None and stage is not None:
            raise ValueError("Only one argument of version and stage can be not None")

        return ActiveArtifact(self.__api_client, self.__project_key, name, version, stage).load_model()

    @property
    def options(self) -> ConnectionOptions:
        return self.__options

    @property
    def api_client(self) -> Client:
        return self.__api_client

    @staticmethod
    def __get_default_options() -> ConnectionOptions:
        options = ConnectionOptions()
        options.server_url = 'http://localhost:9000/api/v1'
        options.api_key = os.environ.get('MLAIDE_API_KEY')
        return options

    @staticmethod
    def __merge_options(target: ConnectionOptions, source: ConnectionOptions) -> ConnectionOptions:
        merged = dict()
        merged.update(target.to_dict())
        merged.update(source.to_dict())

        return ConnectionOptions.from_dict(merged)

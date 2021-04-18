from . import _model_deser
from ._api_client import Client
from ._api_client.api import run_api, artifact_api, experiment_api
from ._api_client.dto import ArtifactDto, ExperimentDto, ExperimentStatusDto, RunDto, StatusDto
from .model import Artifact, ArtifactRef, Run, RunStatus
from .mapper import dto_to_run, run_to_dto, dto_to_artifact

from datetime import datetime
from typing import Dict, List, Optional, Union
from io import BytesIO
from pathlib import Path
from os.path import relpath


class ActiveRun(object):
    """This class provides access to runs that are stored in ML Aide"""

    __api_client: Client
    __run: Run
    __project_key: str

    def __init__(self,
                 api_client: Client,
                 project_key: str,
                 experiment_key: Optional[str] = None,
                 run_name: str = None,
                 used_artifacts: Optional[List[ArtifactRef]] = None,
                 auto_create_experiment: bool = True):
        self.__api_client = api_client
        self.__project_key = project_key

        if auto_create_experiment and experiment_key is not None:
            self.__create_experiment_if_not_present(project_key, experiment_key)

        self.__run = self.__create_new_run(experiment_key, run_name, used_artifacts)

    def __create_new_run(self,
                         experiment_key: str = None,
                         run_name: str = None,
                         used_artifacts: Optional[List[ArtifactRef]] = None) -> Run:
        run = Run(name=run_name, status=RunStatus.RUNNING)
        run_to_create = run_to_dto(run, experiment_key, used_artifacts)

        created_run: RunDto = run_api.create_run(
            client=self.__api_client,
            project_key=self.__project_key,
            run=run_to_create
        )

        return dto_to_run(created_run)

    def __create_experiment_if_not_present(self, project_key: str, experiment_key: str):
        experiment = experiment_api.get_experiment(client=self.__api_client,
                                                   project_key=project_key,
                                                   experiment_key=experiment_key)

        if experiment is None:
            experiment = ExperimentDto(key=experiment_key, name=experiment_key, status=ExperimentStatusDto.IN_PROGRESS)
            experiment_api.create_experiment(client=self.__api_client, project_key=project_key, experiment=experiment)

    @property
    def run(self) -> Run:
        # Return a deep copy to avoid changing anything by the client
        return Run(
            start_time=self.__run.start_time,
            end_time=self.__run.end_time,
            status=self.__run.status,
            metrics=self.__run.metrics,
            parameters=self.__run.parameters,
            key=self.__run.key,
            name=self.__run.name
        )

    def log_metric(self, key: str, value) -> Run:
        """Logs a metric

        Arguments:
            key: The key of the metric.
            value: The value of the metric. The value can be any type that is JSON serializable.
        """
        self.__run.metrics[key] = value
        run_api.update_run_metrics(
            client=self.__api_client,
            project_key=self.__project_key,
            run_key=self.__run.key,
            metrics={key: value})
        return self.__run

    def log_parameter(self, key: str, value) -> Run:
        """Logs a parameter

        Arguments:
            key: The key of the parameter.
            value: The value of the parameter. The value must be a scalar value (e.g. string, int, float, ...).
        """
        self.__run.parameters[key] = value
        run_api.update_run_parameters(
            client=self.__api_client,
            project_key=self.__project_key,
            run_key=self.__run.key,
            parameters={key: value})
        return self.__run

    def log_model(self, model, model_name: str, metadata: Optional[Dict[str, str]] = None):
        """Creates a new artifact with type 'model'. The artifact will be registered as model.

        Arguments:
            model: The model. The model must be serializable.
            model_name: The name of the model. The name will be used as artifact filename.
            metadata: Some optional metadata that will be attached to the artifact.
        """
        serialized_model = _model_deser.serialize(model)

        artifact = self.create_artifact(name=model_name, artifact_type='model', metadata=metadata)
        self.add_artifact_file(artifact=artifact, file=serialized_model, filename='model.pkl')

        artifact_api.create_model(
            client=self.__api_client,
            project_key=self.__project_key,
            artifact_name=artifact.name,
            artifact_version=artifact.version)

    def create_artifact(self, name: str, artifact_type: str, metadata: Optional[Dict[str, str]]) -> Artifact:
        """Creates a new artifact. If an artifact with the same name already exists, a new artifact with the
        next available version number will be registered.

        Arguments:
            name: The name of the artifact.
            artifact_type: The artifact type.
            metadata: Some optional metadata that will be attached to the artifact.
        """
        artifact_dto = ArtifactDto(name=name, type=artifact_type, metadata=metadata, run_key=self.__run.key)

        artifact_dto = artifact_api.create_artifact(
            client=self.__api_client,
            project_key=self.__project_key,
            artifact=artifact_dto)

        return dto_to_artifact(artifact_dto)

    def add_artifact_file(self, artifact: Artifact, file: Union[str, BytesIO], filename: str = None):
        """Add a file to an existing artifact. To add multiple file, specify a directory or invoke this function
        multiple times.

        Arguments:
            artifact: The artifact to which the file should be added.
            file: The file that should be added. This can be a io.BytesIO object or a string to a file or directory.
            filename: The filename. If the file is of type BytesIO the filename must be specified. If the file is a
                string, the original filename will be the default.
        """
        artifact_api.upload_file(
            client=self.__api_client,
            project_key=self.__project_key,
            artifact_name=artifact.name,
            artifact_version=artifact.version,
            filename=filename if filename is not None else ActiveRun.__extract_filename(file),
            file=ActiveRun.__normalize_file(file))

    @staticmethod
    def __extract_filename(file: Union[str, BytesIO]) -> str:
        if isinstance(file, str):
            return relpath(file)

        raise Exception('filename must be provided if provided file is of type io.BytesIO')

    @staticmethod
    def __normalize_file(file: Union[str, BytesIO]) -> BytesIO:
        if isinstance(file, str):  # Read the file behind the string/path
            if file.startswith('http://') or file.startswith('https://'):  # The file must be downloaded
                pass
                # TODO: Download file

            else:  # The file must be read from filesystem
                path = Path(file)

                if path.is_file():  # check if it is only a single file
                    file_bytes = path.read_bytes()
                    return BytesIO(file_bytes)

                elif path.is_dir():  # ... or is it a directory?
                    pass
                    # TODO: Read all files from directory

        else:  # The passed file is already of type BytesIO
            return file

    def set_completed_status(self) -> Run:
        """Sets the status of the current run as completed."""
        return self._set_status(RunStatus.COMPLETED)

    def set_failed_status(self) -> Run:
        """Sets the status of the current run as failed."""
        return self._set_status(RunStatus.FAILED)

    def _set_status(self, status: RunStatus) -> Run:
        self.__run.end_time = datetime.now()
        self.__run.status = status
        run_api.partial_update_run(
            client=self.__api_client,
            project_key=self.__project_key,
            run_key=self.__run.key,
            run=RunDto(
                status=StatusDto(status.name)
            )
        )
        return self.__run

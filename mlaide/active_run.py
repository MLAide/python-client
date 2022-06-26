from mlaide._api_client.dto.file_hash_dto import FileHashDto
from . import _model_deser, _file_utils
from ._api_client import Client
from ._api_client.api import run_api, artifact_api
from ._api_client.dto import ArtifactDto, ExperimentDto, RunDto, StatusDto
from .model import Artifact, ArtifactRef, Git, Run, RunStatus, NewArtifact, InMemoryArtifactFile, LocalArtifactFile, Experiment
from .mapper import dto_to_run, run_to_dto, dto_to_artifact

from datetime import datetime
from typing import Dict, List, Optional, Union
from io import BytesIO
from pathlib import Path
from os import getcwd, path


def get_file_hash(file: Union[InMemoryArtifactFile, LocalArtifactFile]) -> FileHashDto:
    if isinstance(file, InMemoryArtifactFile):
        return FileHashDto(file.file_name, _file_utils.calculate_checksum_of_bytes(file.file_content))
    elif isinstance(file, LocalArtifactFile):
        file_name = Path.joinpath(Path(getcwd()), file.file_name)
        absolute_file_path = str(file_name.absolute())
        file_hash = _file_utils.calculate_checksum_of_file(absolute_file_path)
        return FileHashDto(extract_filename(file.file_name), file_hash)


def extract_filename(file: Union[str, BytesIO]) -> str:
    if isinstance(file, str):
        return path.relpath(file)

    raise Exception('filename must be provided if provided file is of type io.BytesIO')


def get_file_content(file: Union[str, BytesIO]) -> BytesIO:
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


class ActiveRun(object):
    """This class provides access to runs that are stored in ML Aide"""

    __api_client: Client
    __run: Run
    __project_key: str

    def __init__(self,
                 api_client: Client,
                 project_key: str,
                 experiment: Experiment,
                 run_name: str,
                 git: Optional[Git] = None,
                 used_artifacts: Optional[List[ArtifactRef]] = None):
        self.__api_client = api_client
        self.__project_key = project_key

        self.__run = self.__create_new_run(experiment.key, run_name, git, used_artifacts)

    def __create_new_run(self,
                         experiment_key: str,
                         run_name: str,
                         git: Optional[Git] = None,
                         used_artifacts: Optional[List[ArtifactRef]] = None) -> Run:
        run = Run(name=run_name, status=RunStatus.RUNNING, git=git)
        run_to_create = run_to_dto(run, experiment_key, used_artifacts)

        created_run: RunDto = run_api.create_run(
            client=self.__api_client,
            project_key=self.__project_key,
            run=run_to_create
        )

        return dto_to_run(created_run)

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

    def log_metric_epoch(self, key: str, epoch: str, value) -> Run:
        """Logs a metric for an epoch

        Arguments:
            key: The key of the metric.
            epoch: The corresponding epoch.
            value: The value of the metric. The value can be any type that is JSON serializable.
        """
        if self.__run.metrics.get(key):
            new_dict = dict(self.__run.metrics.get(key))
            new_dict.update({epoch: value})
            self.__run.metrics[key] = new_dict
        else:
            self.__run.metrics[key] = {epoch: value}
        run_api.update_run_metrics(
            client=self.__api_client,
            project_key=self.__project_key,
            run_key=self.__run.key,
            metrics={key: self.__run.metrics[key]})
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
        files = _model_deser.serialize(model)

        new_artifact = NewArtifact(
            name=model_name,
            type='model',
            metadata=metadata,
            files=files
        )
        artifact = self.add_artifact(new_artifact)

        artifact_api.create_model(
            client=self.__api_client,
            project_key=self.__project_key,
            artifact_name=artifact.name,
            artifact_version=artifact.version)

    def add_artifact(self, artifact: NewArtifact) -> Artifact:
        """Adds an artifact to the current run. If an artifact with the same name and the same files
        is already existing in another experiment the existing artifact will be reference. Thus, uploading
        the files of this artifact won't be necessary. If the artifact does not exist, it will be created
        and all files of the artifact will be uploaded.

        Arguments:
            artifact: The artifact should be created or referenced.
        """
        files_with_file_hashes = [(file, get_file_hash(file)) for file in artifact.files]
        file_hashes = [file_with_hash[1] for file_with_hash in files_with_file_hashes]
        
        # check if an artifact with these files already exists (in any other experiment)
        artifact_dto: ArtifactDto = artifact_api.find_artifact_by_file_hashes(
            client=self.__api_client,
            project_key=self.__project_key,
            artifact_name=artifact.name,
            files=file_hashes)

        if artifact_dto is None:
            # artifact does not exist, yet - create artifact and upload all files of the artifact
            new_artifact = self.__create_artifact(artifact.name, artifact.type, artifact.metadata)
            for file_with_hash in files_with_file_hashes:
                file = file_with_hash[0]
                file_hash = file_with_hash[1]
                if isinstance(file, InMemoryArtifactFile):
                    self.__add_artifact_file(new_artifact, file_hash.fileHash, file.file_content, file.file_name)
                elif isinstance(file, LocalArtifactFile):
                    self.__add_artifact_file(new_artifact, file_hash.fileHash, file.file_name)

            return new_artifact

        else:
            # TODO: Merge artifact metadata into the existing metadata of the artifact

            # an artifact with the same content already exists - just link artifact to this run
            run_api.attach_artifact_to_run(
                client=self.__api_client,
                artifact_name=artifact_dto.name,
                artifact_version=artifact_dto.version,
                project_key=self.__project_key,
                run_key=self.__run.key
            )

            return dto_to_artifact(artifact_dto)

    def __create_artifact(self, name: str, artifact_type: str, metadata: Optional[Dict[str, str]]) -> Artifact:
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

    def __add_artifact_file(self, artifact: Artifact, file_hash: str, file: Union[str, BytesIO], filename: str = None):
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
            filename=filename if filename is not None else extract_filename(file),
            file_hash=file_hash,
            file=get_file_content(file))

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

from modelversioncontrol.run import Run, RunStatus
from . import _model_serializer
from ._api_client import Client
from ._api_client.api import runs as runs_client, artifacts as artifacts_client
from ._api_client.models import \
    ExperimentRef as ExperimentRefDto, \
    Model as ModelDto, \
    Run as RunDto, \
    Status as RunStatusDto, \
    Error as ErrorDto
from ._api_client.errors import ApiResponseError
from datetime import datetime
from typing import Union


class ActiveRun(object):
    __api_client: Client
    __run: Run
    __project_id: str

    def __init__(self, api_client: Client, project_id: str, experiment_key: str = None, run_name: str = None):
        self.__api_client = api_client
        self.__project_id = project_id
        self.__run = self.__create_new_run(experiment_key, run_name)

    def __create_new_run(self, experiment_key: str = None, run_name: str = None) -> Run:
        run_to_create = RunDto(
            created_at=None,
            end_time=None,
            experiment_refs=[ExperimentRefDto(experiment_key)] if experiment_key is not None else None,
            id=None,
            metrics=None,
            name=run_name,
            parameters=None,
            start_time=None,
            status=RunStatusDto.RUNNING,
            user=None
        )
        try:
            created_run: Union[RunDto, ErrorDto] = runs_client.create_run(
                client=self.__api_client,
                project_id=self.__project_id,
                json_body=run_to_create
            )
        except ApiResponseError as error:
            print(error)
            print(error.response.status_code)
            print(error.response.json())
            raise

        return Run(
            name=created_run.name,
            status=RunStatus[created_run.status.name],
            parameters={} if created_run.parameters is None else created_run.parameters,
            metrics={} if created_run.metrics is None else created_run.metrics,
            start_time=created_run.start_time,
            end_time=created_run.end_time,
            id=created_run.id,
        )

    @property
    def run(self) -> Run:
        # Return a deep copy to avoid changing anything by the client
        return Run(
            start_time=self.__run.start_time,
            end_time=self.__run.end_time,
            status=self.__run.status,
            metrics=self.__run.metrics,
            parameters=self.__run.parameters,
            id=self.__run.id,
            name=self.__run.name
        )

    def log_metric(self, key: str, value) -> Run:
        self.__run.metrics[key] = value
        runs_client.update_run_metrics(
            client=self.__api_client,
            project_id=self.__project_id,
            run_id=self.__run.id,
            metrics={key: value})
        return self.__run

    def log_parameter(self, key: str, value) -> Run:
        self.__run.parameters[key] = value
        runs_client.update_run_parameters(
            client=self.__api_client,
            project_id=self.__project_id,
            run_id=self.__run.id,
            parameters={key: value})
        return self.__run

    def log_model(self, model, model_name):
        serialized_model = _model_serializer.serialize(model)

        model = ModelDto(name=model_name, run_id=self.__run.id)
        model = artifacts_client.create_model(client=self.__api_client, project_id=self.__project_id, json_body=model)

        try:
            artifacts_client.upload_artifact_binary(
                client=self.__api_client,
                project_id=self.__project_id,
                model_name=model.name,
                model_version=1, # model.version,
                binary=serialized_model)
        except ApiResponseError as error:
            print(error)
            print(error.response.status_code)
            print(error.response.text)
            raise

    def set_completed_status(self) -> Run:
        return self._set_status(RunStatus.COMPLETED)

    def set_failed_status(self) -> Run:
        return self._set_status(RunStatus.FAILED)

    def _set_status(self, status: RunStatus) -> Run:
        self.__run.end_time = datetime.now()
        self.__run.status = status
        runs_client.partial_update_run(
            client=self.__api_client,
            project_id=self.__project_id,
            run_id=self.__run.id,
            json_body=RunDto(
                status=RunStatusDto(status.name)
            )
        )
        return self.__run

from modelversioncontrol.experiment import Experiment, ExperimentStatus
from modelversioncontrol.api_client import Client
from modelversioncontrol.api_client.api import experiments as experiments_client
from modelversioncontrol.api_client.models import \
    Experiment as ExperimentDto, \
    Status as ExperimentStatusDto, \
    Error as ErrorDto
from modelversioncontrol.api_client.errors import ApiResponseError
from datetime import datetime
from typing import Union


class ActiveExperiment(object):
    __api_client: Client
    __experiment: Experiment
    __experiment_name: str
    __project_id: str

    def __init__(self, api_client: Client, project_id: str, experiment_name: str = None):
        self.__api_client = api_client
        self.__project_id = project_id
        self.__experiment_name = experiment_name
        self.__experiment = self.__create_new_experiment()

    def __create_new_experiment(self) -> Experiment:
        experiment_to_create = ExperimentDto(
            start_time=None,
            end_time=None,
            status=ExperimentStatusDto.RUNNING,
            metrics=None,
            parameters=None,
            id=None,
            name=self.__experiment_name,
            created_at=None,
            user=None
        )
        try:
            created_experiment: Union[ExperimentDto, ErrorDto] = experiments_client.create_experiment(
                client=self.__api_client,
                project_id=self.__project_id,
                json_body=experiment_to_create
            )
        except ApiResponseError as error:
            print(error)
            raise

        return Experiment(
            name=created_experiment.name,
            status=ExperimentStatus[created_experiment.status.name],
            parameters={} if created_experiment.parameters is None else created_experiment.parameters.to_dict(),
            metrics={} if created_experiment.metrics is None else created_experiment.metrics.to_dict(),
            start_time=created_experiment.start_time,
            end_time=created_experiment.end_time,
            id=created_experiment.id,
        )

    @property
    def experiment(self) -> Experiment:
        # Return a deep copy to avoid changing anything by the client
        return Experiment(
            start_time=self.__experiment.start_time,
            end_time=self.__experiment.end_time,
            status=self.__experiment.status,
            metrics=self.__experiment.metrics,
            parameters=self.__experiment.parameters,
            id=self.__experiment.id,
            name=self.__experiment.name
        )

    def add_metric(self, key: str, value) -> Experiment:
        self.__experiment.metrics[key] = value
        experiments_client.update_experiment_metrics(
            client=self.__api_client,
            project_id=self.__project_id,
            experiment_id=self.__experiment.id,
            metrics={key: value})
        return self.__experiment

    def add_parameter(self, key: str, value) -> Experiment:
        self.__experiment.parameters[key] = value
        experiments_client.update_experiment_parameters(
            client=self.__api_client,
            project_id=self.__project_id,
            experiment_id=self.__experiment.id,
            parameters={key: value})
        return self.__experiment

    def set_completed_status(self) -> Experiment:
        return self._set_status(ExperimentStatus.COMPLETED)

    def set_failed_status(self) -> Experiment:
        return self._set_status(ExperimentStatus.FAILED)

    def _set_status(self, status: ExperimentStatus) -> Experiment:
        self.__experiment.end_time = datetime.now()
        self.__experiment.status = status
        experiments_client.partial_update_experiment(
            client=self.__api_client,
            project_id=self.__project_id,
            experiment_id=self.__experiment.id,
            json_body=ExperimentDto(
                status=ExperimentStatusDto(status.name)
            )
        )
        return self.__experiment

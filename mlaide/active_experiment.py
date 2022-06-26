from mlaide._api_client.dto.experiment_dto import ExperimentDto
from mlaide.active_run import ActiveRun
from . import mapper
from ._api_client import Client
from ._api_client.api import experiment_api
from .model import Experiment, ArtifactRef
from .git_resolver import get_git_metadata

from dataclasses import replace
from typing import List


class ActiveExperiment(object):
    """This class provides access to a experiment of ML Aide"""

    __api_client: Client
    __project_key: str
    __experiment: Experiment

    def __init__(self,
                 api_client: Client,
                 project_key: str,
                 experiment_name: str):
        self.__api_client = api_client
        self.__project_key = project_key
        self.__experiment = self.__create_experiment(experiment_name)

    def __create_experiment(self, experiment_name: str) -> Experiment:
        experiment_dto = ExperimentDto(name=experiment_name)
        experiment_dto = experiment_api.create_experiment(client=self.__api_client, project_key=self.__project_key, experiment=experiment_dto)
        return mapper.dto_to_experiment(experiment_dto)

    @property
    def experiment(self) -> Experiment:
        # Return a deep copy to avoid changing anything by the client
        return replace(self.__experiment)

    def start_new_run(self,
                      run_name: str = None,
                      used_artifacts: List[ArtifactRef] = None) -> ActiveRun:
        """Creates and starts a new run, that will be assigned to the specified experiment. The run object can be used
        to log all necessary information.

        Arguments:
            experiment_key: The key of the experiment, that the new run should be assigned to. If `None` a new, random
                experiment will be created.
            run_name: The name of the run. The name helps to identify the run for humans. If `None` a random name will
                be used.
            used_artifacts: An optional list of `ArtifactRef` that references artifacts, that are used as input for
                this run. This information will help to create and visualize the experiment lineage.
            auto_create_experiment: Specifies whether the experiment (see `experiment_key`) should be created if it
                does not exist or not. If `auto_create_experiment` is `False` and the experiment does not exist an error
                will be raised.

        Returns:
            This object encapsulates the newly created run and provides functions to log all information \
            that belongs to the run.
        """
        return ActiveRun(api_client=self.__api_client,
                         project_key=self.__project_key,
                         experiment=self.__experiment,
                         run_name=run_name,
                         git=get_git_metadata(),
                         used_artifacts=used_artifacts)
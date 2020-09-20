import datetime
from enum import Enum
from typing import Dict
from dataclasses import dataclass


class ExperimentStatus(Enum):
    RUNNING = 1,
    FAILED = 2,
    COMPLETED = 3,


@dataclass
class Experiment(object):
    id: str
    name: str
    start_time: datetime
    end_time: datetime
    status: ExperimentStatus
    metrics: Dict
    parameters: Dict[str, str]

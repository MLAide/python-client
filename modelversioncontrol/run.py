import datetime
from enum import Enum
from typing import Dict
from dataclasses import dataclass


class RunStatus(Enum):
    RUNNING = 1,
    FAILED = 2,
    COMPLETED = 3,


@dataclass
class Run(object):
    key: int
    name: str
    start_time: datetime
    end_time: datetime
    status: RunStatus
    metrics: Dict
    parameters: Dict[str, str]

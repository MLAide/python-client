import datetime
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass, field
from . import Git


class RunStatus(str, Enum):
    RUNNING = 'RUNNING',
    FAILED = 'FAILED',
    COMPLETED = 'COMPLETED',


@dataclass
class Run(object):
    git: Optional[Git] = None
    key: Optional[int] = None
    name: Optional[str] = None
    start_time: datetime = None
    end_time: datetime = None
    status: Optional[RunStatus] = None
    metrics: Dict[str, any] = field(default_factory=dict)
    parameters: Dict[str, str] = field(default_factory=dict)

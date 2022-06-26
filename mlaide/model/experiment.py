import datetime
from dataclasses import dataclass
from typing import Collection, Dict, List, Optional
from . import ArtifactFile, Model, UserRef


@dataclass
class Experiment(object):
    created_at: datetime = None
    key: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None

from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Collection, Dict, Optional
from . import UserRef


class ModelStage(Enum):
    NONE = 'NONE',
    STAGING = 'STAGING',
    PRODUCTION = 'PRODUCTION',
    ABANDONED = 'ABANDONED',
    DEPRECATED = 'DEPRECATED'


@dataclass
class ModelRevision(object):
    newStage: ModelStage
    oldStage: ModelStage
    created_at: datetime = None
    created_by: Optional[UserRef] = None
    note: str = None


@dataclass
class Model(object):
    created_at: datetime = None
    created_by: Optional[UserRef] = None
    modelRevisions: Optional[Collection[ModelRevision]] = None
    metadata: Optional[Dict[str, str]] = None
    stage: Optional[ModelStage] = None
    updated_at: datetime = None

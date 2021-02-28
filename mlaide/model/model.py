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
    new_stage: ModelStage
    old_stage: ModelStage
    created_at: Optional[datetime] = None
    created_by: Optional[UserRef] = None
    note: Optional[str] = None


@dataclass
class Model(object):
    created_at: Optional[datetime] = None
    created_by: Optional[UserRef] = None
    model_revisions: Optional[Collection[ModelRevision]] = None
    metadata: Optional[Dict[str, str]] = None
    stage: Optional[ModelStage] = None
    updated_at: Optional[datetime] = None

import datetime
from dataclasses import dataclass
from typing import Collection, Dict, Optional
from . import ArtifactFile, Model, UserRef


@dataclass
class Artifact(object):
    created_at: datetime = None
    created_by: Optional[UserRef] = None
    files: Optional[Collection[ArtifactFile]] = None
    metadata: Optional[Dict[str, str]] = None
    model: Optional[Model] = None
    name: Optional[str] = None
    run_key: Optional[int] = None
    run_name: Optional[str] = None
    type: Optional[str] = None
    updated_at: datetime = None
    version: Optional[int] = None

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined
from datetime import datetime
from typing import Any, Dict, List, Optional

from .helper import datetime_field


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class ArtifactFileDto:
    fileId: str
    fileName: str


@dataclass
class ModelRevisionDto(object):
    newStage: str
    oldStage: str
    created_at: Optional[datetime] = datetime_field()
    created_by: Optional[Dict[Any, Any]] = None
    note: str = None


@dataclass
class ModelDto(object):
    created_at: Optional[datetime] = datetime_field()
    created_by: Optional[Dict[Any, Any]] = None
    modelRevisions: Optional[List[ModelRevisionDto]] = None
    metadata: Optional[Dict[str, str]] = None
    stage: Optional[str] = None
    updated_at: Optional[datetime] = datetime_field()


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class ArtifactDto:
    created_at: Optional[datetime] = datetime_field()
    created_by: Optional[Dict[Any, Any]] = None
    files: Optional[List[ArtifactFileDto]] = None
    metadata: Optional[Dict[str, str]] = None
    model: Optional[ModelDto] = None
    name: Optional[str] = None
    run_key: Optional[str] = None
    run_name: Optional[str] = None
    type: Optional[str] = None
    updated_at: Optional[datetime] = datetime_field()
    version: Optional[int] = None

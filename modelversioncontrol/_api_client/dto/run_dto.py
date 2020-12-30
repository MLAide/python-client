from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined
import datetime
from typing import Any, Dict, Optional, List

from .artifact_ref_dto import ArtifactRefDto
from .experiment_ref_dto import ExperimentRefDto
from .helper import datetime_field
from .status_dto import StatusDto


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class RunDto:
    created_at: Optional[datetime.datetime] = datetime_field()
    created_by: Optional[Dict[Any, Any]] = None
    end_time: Optional[datetime.datetime] = datetime_field()
    experiment_refs: Optional[List[ExperimentRefDto]] = None
    key: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime.datetime] = datetime_field()
    status: Optional[StatusDto] = None
    used_artifacts: Optional[List[ArtifactRefDto]] = None

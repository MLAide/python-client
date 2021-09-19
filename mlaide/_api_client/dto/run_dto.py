from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, LetterCase, Undefined
import datetime
from typing import Any, Dict, Optional, List

from .artifact_ref_dto import ArtifactRefDto
from .git_dto import GitDto
from .experiment_ref_dto import ExperimentRefDto
from .status_dto import StatusDto
from .helper import datetime_field, ExtendedDtoSerializer


@dataclass
class RunDto(ExtendedDtoSerializer, DataClassJsonMixin):
    dataclass_json_config = config(
        letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE
    )['dataclasses_json']

    created_at: Optional[datetime.datetime] = datetime_field()
    created_by: Optional[Dict[Any, Any]] = None
    end_time: Optional[datetime.datetime] = datetime_field()
    experiment_refs: Optional[List[ExperimentRefDto]] = None
    git: Optional[GitDto] = None
    key: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime.datetime] = datetime_field()
    status: Optional[StatusDto] = None
    used_artifacts: Optional[List[ArtifactRefDto]] = None

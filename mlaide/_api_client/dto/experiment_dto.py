from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, LetterCase, Undefined
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .helper import datetime_field, ExtendedDtoSerializer


@dataclass
class ExperimentDto(ExtendedDtoSerializer, DataClassJsonMixin):
    dataclass_json_config = config(
        letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE
    )['dataclasses_json']

    created_at: Optional[datetime] = datetime_field()
    key: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None

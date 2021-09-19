import datetime
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, dataclass_json, LetterCase, Undefined

from .helper import datetime_field, ExtendedDtoSerializer


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class GitDto(ExtendedDtoSerializer, DataClassJsonMixin):
    dataclass_json_config = config(
        letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE
    )['dataclasses_json']

    is_dirty: bool
    commit_time: datetime.datetime = datetime_field()
    commit_hash: str = None
    repository_uri: str = None

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined
from typing import Union


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class ArtifactRefDto(object):
    name: str
    version: Union[int, str, None] = None

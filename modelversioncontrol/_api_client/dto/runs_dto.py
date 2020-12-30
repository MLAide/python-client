from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined

from .run_dto import RunDto


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class ExperimentsDto:
    items: RunDto

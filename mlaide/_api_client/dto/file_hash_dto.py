from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, LetterCase, Undefined

from .helper import ExtendedDtoSerializer


@dataclass
class FileHashDto(ExtendedDtoSerializer, DataClassJsonMixin):
    dataclass_json_config = config(
        letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE
    )['dataclasses_json']

    fileName: str
    fileHash: str

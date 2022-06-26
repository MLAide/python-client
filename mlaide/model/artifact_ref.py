from dataclasses import dataclass
from typing import Union


@dataclass
class ArtifactRef(object):
    name: str
    version: Union[int, None] = None


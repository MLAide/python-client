from dataclasses import dataclass
from typing import Collection, Dict, Optional, Union
from . import InMemoryArtifactFile, LocalArtifactFile


@dataclass
class NewArtifact(object):
    name: str
    type: str
    files: Optional[Collection[Union[InMemoryArtifactFile, LocalArtifactFile]]] = None
    metadata: Optional[Dict[str, str]] = None

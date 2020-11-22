from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Union


@dataclass
class ArtifactRef(object):
    name: str
    version: Union[int, str, None] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.name is not None:
            result["name"] = self.name
        if self.version is not None:
            result["version"] = self.version

        return result

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ArtifactRef:
        name = d["name"]
        version = d["version"]

        return ArtifactRef(name=name, version=version)

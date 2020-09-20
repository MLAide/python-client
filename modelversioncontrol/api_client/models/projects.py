from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, cast

from .project import Project


@dataclass
class Projects:
    """  """

    items: Project

    def to_dict(self) -> Dict[str, Any]:
        items = self.items.to_dict()

        return {
            "items": items,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Projects:
        items = Project.from_dict(d["items"])

        return Projects(items=items,)

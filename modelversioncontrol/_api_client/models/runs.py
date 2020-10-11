from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, cast

from .run import Run


@dataclass
class Experiments:
    """  """

    items: Run

    def to_dict(self) -> Dict[str, Any]:
        items = self.items.to_dict()

        return {
            "items": items,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Experiments:
        items = Run.from_dict(d["items"])

        return Experiments(items=items,)
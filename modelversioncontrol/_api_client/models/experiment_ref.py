from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ExperimentRef:
    experimentKey: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experimentKey": self.experimentKey
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ExperimentRef:
        experiment_key = d["experimentKey"]

        return ExperimentRef(experimentKey=experiment_key)

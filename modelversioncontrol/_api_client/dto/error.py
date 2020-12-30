from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Error:
    """  """

    code: int
    message: str

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        message = self.message

        return {
            "code": code,
            "message": message,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Error:
        code = d["code"]

        message = d["message"]

        return Error(code=code, message=message,)

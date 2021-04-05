from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, cast, Optional
from httpx import Response


@dataclass
class Error:
    """  """

    code: int
    message: Optional[str] = None

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

    @staticmethod
    def from_response(response: Response):
        # todo: Implement proper error response parsing
        response_body = cast(Dict[str, Any], response.json())

        try:
            error = Error.from_dict(response_body)
        except KeyError:
            print(response.json())
            error = Error(code=response.status_code)

        return error

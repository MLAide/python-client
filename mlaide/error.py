from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, cast, Optional
from httpx import Response


@dataclass
class HttpError:
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
    def from_dict(d: Dict[str, Any]) -> HttpError:
        code = d["code"]
        message = d["message"]

        return HttpError(code=code, message=message)

    @staticmethod
    def from_response(response: Response):
        if response.text:
            try:
                response_body = cast(Dict[str, Any], response.json())
                error = HttpError.from_dict(response_body)
            except (KeyError, ValueError):
                error = HttpError(code=response.status_code)
        else:
            error = HttpError(code=response.status_code)

        return error


class MLAideError(Exception):
    http_error: HttpError
    """Base class for exceptions in ML Aide.
    
    Attributes:
        http_error: Details about the HTTP error, if the error was raised for an invalid HTTP response.
    """

    def __init__(self, http_error: HttpError = None):
        self.http_error = http_error


class InputError(MLAideError):
    """Exception raised for errors in the input."""


class NotFoundError(MLAideError):
    """Exception raised for errors where the requested object does not exist."""


class InvalidAuthorizationError(MLAideError):
    """Exception raised for invalid authorization (api key)."""
    pass


class NotAuthorizedError(MLAideError):
    """Exception raised for not sufficient permissions."""
    pass


class ServerError(MLAideError):
    """Exception raised for ML Aide server errors."""
    pass

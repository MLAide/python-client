from mlaide.error import *
from httpx import Response


def assert_response_status(response: Response, is_404_valid: bool = False):
    if response.status_code == 404 and is_404_valid:
        return

    elif response.status_code == 400:
        raise InputError(_http_error(response))

    elif response.status_code == 401:
        raise InvalidAuthorizationError(_http_error(response))

    elif response.status_code == 403:
        raise NotAuthorizedError(_http_error(response))

    elif response.status_code == 404:
        raise NotFoundError(_http_error(response))

    elif response.status_code >= 500:
        raise ServerError(_http_error(response))


def _http_error(response: Response):
    return HttpError.from_response(response)

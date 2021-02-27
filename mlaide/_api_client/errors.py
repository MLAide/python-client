from httpx import Response
from .dto import Error


class ApiResponseError(Exception):
    """ An exception raised when an unknown response occurs """

    def __init__(self, *, response: Response, error: Error = None):
        super().__init__()
        self.response: Response = response
        self.error: Error = error


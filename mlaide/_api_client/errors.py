from httpx import Response


class ApiResponseError(Exception):
    """ An exception raised when an unknown response occurs """

    def __init__(self, *, response: Response, error=None):
        super().__init__()
        self.response: Response = response
        self.error = error


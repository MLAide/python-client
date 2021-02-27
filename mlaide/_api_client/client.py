from dataclasses import dataclass
from typing import Dict


@dataclass
class Client:
    """ A class for keeping track of data related to the API """

    base_url: str

    def get_headers(self) -> Dict[str, str]:
        """ Get headers to be used in all endpoints """
        return {}


@dataclass
class AuthenticatedClient(Client):
    """ A Client which has been authenticated for use on secured endpoints """

    api_key: str

    def get_headers(self) -> Dict[str, str]:
        """ Get headers to be used in authenticated endpoints """
        return {"x-api-key": f"{self.api_key}"}

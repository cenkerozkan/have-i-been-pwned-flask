import os
from logging import Logger

import requests
from requests import Response
from dotenv import load_dotenv
from pprint import pprint

from decorators.sinlgeton import singleton
from exceptions.no_hibp_key_found_exception import NoHibpKeyFoundException
from util.logger import get_logger
from model.hibp_breached_account_model import HibpBreachedAccountModel

load_dotenv()

@singleton
class HaveIBeenPwnedExecutor:
    _API_VERSION: str = "v3"
    _BASE_URL: str = f"https://haveibeenpwned.com/api/{_API_VERSION}"
    _logger = get_logger(__name__)

    @property
    def api_version(self) -> str:
        pass

    @api_version.setter
    def api_version(self, value: str) -> None:
        self._API_VERSION = value

    @api_version.getter
    def api_version(self) -> str:
        return self._API_VERSION

    @classmethod
    def get_breached_accounts(
            cls,
            email: str,
            truncate_response: bool = False,
    ) -> HibpBreachedAccountModel:
        hibp_key: str = os.getenv("HIBP_API_KEY")
        if not hibp_key:
            raise NoHibpKeyFoundException("HIBP_KEY environment variable not set")
        """
        Retrieves breached account information for a given email address.

        :param email: The email address to check for breaches.
        :param truncate_response: If True, the response will be truncated to reduce data size.
        :return: An instance of HibpBreachedAccountModel containing breach details.
        """
        request_url: str = f"{cls._BASE_URL}/breachedaccount/{email}?truncateResponse={truncate_response}"
        headers: dict = {"hibp-api-key": os.getenv("HIBP_API_KEY")}
        response: Response = requests.get(request_url, headers=headers)
        pprint(response.json())

if __name__ == '__main__':
    obj = HaveIBeenPwnedExecutor()
    obj.get_breached_accounts(email="cen_kan@yahoo.com.tr")

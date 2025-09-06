import os
from typing import Optional, List

import requests
from requests import Response
from dotenv import load_dotenv

from decorators.singleton import singleton
from exceptions.no_hibp_key_found_exception import NoHibpKeyFoundException
from exceptions.hibp_could_not_be_verified_exception import HibpCouldNotBeVerifiedException
from model.hibp_breached_site_model import HibpBreachedSiteModel
from util.logger import get_logger

load_dotenv()

@singleton
class HibpClient:
    _API_VERSION: str = "v3"
    _BASE_URL: str = f"https://haveibeenpwned.com/api/{_API_VERSION}"
    _logger = get_logger(__name__)

    def __init__(self):
        self._BASE_URL = f"https://haveibeenpwned.com/api/{self._API_VERSION}"
        self._logger.debug(f"Initialized with API version: {self._API_VERSION}")

    @property
    def api_version(self) -> str:
        return self._API_VERSION

    @api_version.setter
    def api_version(self, value: str) -> None:
        self._API_VERSION = value
        self._BASE_URL = f"https://haveibeenpwned.com/api/{self._API_VERSION}"
        self._logger.info(f"API version changed to: {value}")

    def get_breached_accounts(
            self,
            email: str,
            truncate_response: bool = False,
    ) -> Optional[List[HibpBreachedSiteModel]] | None:
        """
        Retrieves breached account information for a given email address.
        :param email: The email address to check for breaches.
        :param truncate_response: If True, the response will be truncated to reduce data size.
        :return: A list of HibpBreachedSiteModel objects or None if no breaches found.
        """
        hibp_key: str = os.getenv("HIBP_API_KEY")
        if not hibp_key:
            self._logger.error("No HIBP API key found in environment variables")
            raise NoHibpKeyFoundException()
            
        request_url: str = f"{self._BASE_URL}/breachedaccount/{email}?truncateResponse={str(truncate_response).lower()}"
        headers: dict = {"hibp-api-key": hibp_key}
        
        try:
            self._logger.debug(f"Sending request to: {request_url}")
            response: Response = requests.get(request_url, headers=headers)
            self._logger.debug(f"Response: {response}")
            
            if response.status_code == 200:
                # Convert the JSON response to a list of HibpBreachedSiteModel objects
                return [HibpBreachedSiteModel.model_validate(item) for item in response.json()]
            elif response.status_code == 404:
                self._logger.info(f"No breaches found for email: {email}")
                return None
            elif response.status_code == 401:
                self._logger.error("API key verification failed")
                raise HibpCouldNotBeVerifiedException()
            else:
                self._logger.warning(f"Unexpected status code: {response.status_code}")
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            self._logger.error(f"Request failed: {str(e)}")
            raise

if __name__ == '__main__':
    obj = HibpClient()
    email = "cenkerozkanse@gmail.com.tr"  # Use a test email instead of a real one
    result = obj.get_breached_accounts(email=email)
    if result:
        print(f"Found {len(result)} breaches for {email}")
        for breach in result:
            print(f"- {breach.title} ({breach.breach_date}): {breach.domain}")
    else:
        print(f"No breaches found for {email}")

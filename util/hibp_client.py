import os
from typing import Optional, List, Set

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

    def get_mock_breached_accounts(
            self,
            email: str,
            truncate_response: bool = False,
    ) -> Optional[List[HibpBreachedSiteModel]] | None:
        """
        Returns mock breach data for testing purposes.
        
        Args:
            email: Email address to check (used only for logging)
            truncate_response: Ignored in mock implementation
            
        Returns:
            List of HibpBreachedSiteModel objects with sample breach data or None
        """
        self._logger.info(f"Using mock breach data for email: {email}")
        
        # Simulate some emails having no breaches
        if email.endswith(".gov") or email.endswith(".edu"):
            self._logger.info(f"No breaches found for email: {email} (mock)")
            return None
            
        mock_data = [
            {
                "Name": "Dailymotion",
                "Title": "Dailymotion",
                "Domain": "dailymotion.com",
                "BreachDate": "2016-10-20",
                "AddedDate": "2017-08-07T02:51:12Z",
                "ModifiedDate": "2017-08-07T02:51:12Z",
                "PwnCount": 85176234,
                "Description": "In October 2016, the video sharing platform <a href=\"http://thehackernews.com/2016/12/dailymotion-video-hacked.html\" target=\"_blank\" rel=\"noopener\">Dailymotion suffered a data breach</a>. The attack led to the exposure of more than 85 million user accounts and included email addresses, usernames and bcrypt hashes of passwords.",
                "LogoPath": "https://logos.haveibeenpwned.com/Dailymotion.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Email addresses",
                    "Passwords",
                    "Usernames"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            {
                "Name": "BlankMediaGames",
                "Title": "BlankMediaGames",
                "Domain": "blankmediagames.com",
                "BreachDate": "2018-12-28",
                "AddedDate": "2019-01-02T05:52:56Z",
                "ModifiedDate": "2019-01-02T06:03:19Z",
                "PwnCount": 7633234,
                "Description": "In December 2018, the Town of Salem website produced by <a href=\"https://blog.dehashed.com/town-of-salem-blankmediagames-hacked/\" target=\"_blank\" rel=\"noopener\">BlankMediaGames suffered a data breach</a>. Reported to HIBP by <a href=\"https://dehashed.com/\" target=\"_blank\" rel=\"noopener\">DeHashed</a>, the data contained 7.6M unique user email addresses alongside usernames, IP addresses, purchase histories and passwords stored as phpass hashes. DeHashed made multiple attempts to contact BlankMediaGames over various channels and many days but had yet to receive a response at the time of publishing.",
                "LogoPath": "https://logos.haveibeenpwned.com/BlankMediaGames.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Browser user agent details",
                    "Email addresses",
                    "IP addresses",
                    "Passwords",
                    "Purchases",
                    "Usernames",
                    "Website activity"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            {
                "Name": "Wattpad",
                "Title": "Wattpad",
                "Domain": "wattpad.com",
                "BreachDate": "2020-06-29",
                "AddedDate": "2020-07-19T22:49:19Z",
                "ModifiedDate": "2020-07-19T22:49:19Z",
                "PwnCount": 268765495,
                "Description": "In June 2020, the user-generated stories website <a href=\"https://www.bleepingcomputer.com/news/security/wattpad-data-breach-exposes-account-info-for-millions-of-users/\" target=\"_blank\" rel=\"noopener\">Wattpad suffered a huge data breach that exposed almost 270 million records</a>. The data was initially sold then published on a public hacking forum where it was broadly shared. The incident exposed extensive personal information including names and usernames, email and IP addresses, genders, birth dates and passwords stored as bcrypt hashes.",
                "LogoPath": "https://logos.haveibeenpwned.com/Wattpad.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Bios",
                    "Dates of birth",
                    "Email addresses",
                    "Genders",
                    "Geographic locations",
                    "IP addresses",
                    "Names",
                    "Passwords",
                    "Social media profiles",
                    "User website URLs",
                    "Usernames"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            {
                "Name": "Kaneva",
                "Title": "Kaneva",
                "Domain": "kaneva.com",
                "BreachDate": "2016-07-01",
                "AddedDate": "2023-12-09T07:00:29Z",
                "ModifiedDate": "2023-12-09T07:00:29Z",
                "PwnCount": 3901179,
                "Description": "In July 2016, now defunct website Kaneva, the service to &quot;build and explore virtual worlds&quot;, suffered a data breach that exposed 3.9M user records. The data included email addresses, usernames, dates of birth and salted MD5 password hashes.",
                "LogoPath": "https://logos.haveibeenpwned.com/Kaneva.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Dates of birth",
                    "Email addresses",
                    "Passwords",
                    "Usernames"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            # Additional mock breaches
            {
                "Name": "LinkedIn",
                "Title": "LinkedIn",
                "Domain": "linkedin.com",
                "BreachDate": "2021-06-22",
                "AddedDate": "2021-06-29T14:35:00Z",
                "ModifiedDate": "2021-06-29T14:35:00Z",
                "PwnCount": 756432198,
                "Description": "In June 2021, LinkedIn experienced a significant data breach affecting over 756 million users. The breach exposed email addresses, phone numbers, work history, and other profile data that was scraped from public profiles.",
                "LogoPath": "https://logos.haveibeenpwned.com/LinkedIn.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Email addresses",
                    "Phone numbers",
                    "Employment details",
                    "Names",
                    "Geographic locations",
                    "Social media profiles"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            {
                "Name": "Dropbox",
                "Title": "Dropbox",
                "Domain": "dropbox.com",
                "BreachDate": "2022-10-13",
                "AddedDate": "2022-11-01T09:12:43Z",
                "ModifiedDate": "2022-11-01T09:12:43Z",
                "PwnCount": 68648009,
                "Description": "In October 2022, Dropbox discovered a breach where attackers gained access to 68 million user records including email addresses and hashed passwords. The company reset passwords for affected users and implemented additional security measures.",
                "LogoPath": "https://logos.haveibeenpwned.com/Dropbox.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Email addresses",
                    "Passwords",
                    "Names"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            },
            {
                "Name": "Adobe",
                "Title": "Adobe",
                "Domain": "adobe.com",
                "BreachDate": "2023-03-15",
                "AddedDate": "2023-03-25T18:22:10Z",
                "ModifiedDate": "2023-03-25T18:22:10Z",
                "PwnCount": 38154113,
                "Description": "In March 2023, Adobe reported a security incident affecting their Creative Cloud service. The breach exposed email addresses, encrypted passwords, and subscription information for over 38 million users.",
                "LogoPath": "https://logos.haveibeenpwned.com/Adobe.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": [
                    "Email addresses",
                    "Passwords",
                    "Subscription details",
                    "Names",
                    "Payment info"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False
            }
        ]
        
        # Convert the mock data to HibpBreachedSiteModel objects
        return [HibpBreachedSiteModel.model_validate(item) for item in mock_data]

if __name__ == '__main__':
    obj = HibpClient()
    email = "cenkerozkanse@gmail.com.tr"  # Use a test email instead of a real one
    # result = obj.get_breached_accounts(email=email)
    result = obj.get_mock_breached_accounts(email=email)
    if result:
        print(f"Found {len(result)} breaches for {email}")
        for breach in result:
            print(f"- {breach.title} ({breach.breach_date}): {breach.domain}")
    else:
        print(f"No breaches found for {email}")

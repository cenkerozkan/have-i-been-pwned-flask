import requests

from decorators.sinlgeton import singleton
from model.hibp_breached_account_model import HibpBreachedAccountModel

@singleton
class HaveIBeenPwnedExecutor:
    _API_VERSION: str = "v3"
    _BASE_URL: str = f"https://haveibeenpwned.com/api/{_API_VERSION}"

    @classmethod
    def get_breached_accounts(cls) -> HibpBreachedAccountModel:
        pass
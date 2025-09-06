from util.hibp_client import HaveIBeenPwnedRequestExecutor
from repository.email_repository import EmailRepository
from repository.pwned_platform_repository import PwnedPlatformRepository

from db.model.email import Email

class PwnChecker:
    def __init__(self):
        self._pwned_request_executor = HaveIBeenPwnedRequestExecutor()
        self._email_repository = EmailRepository()
        self._pwned_platform_repository = PwnedPlatformRepository()

    def _get_all_emails(self):
        emails: list[Email] = self._email_repository.get_all()

    def run(self):
        pass
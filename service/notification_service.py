from typing import List

from decorators.singleton import singleton
from repository.user_repository import UserRepository
from util.email_sender import EmailSender
from util.logger import get_logger
from model.hibp_breached_site_model import HibpBreachedSiteModel


@singleton
class NotificationService:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._user_repository = UserRepository()
        self._email_sender = EmailSender()

    def send_breach_notification(
        self,
        new_breaches: List[HibpBreachedSiteModel]
    ) -> bool:
        """Send notification about new breaches to the user.

        Args:
            email_address: The breached email address
            new_breaches: List of HibpBreachedSiteModel objects containing breach information

        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        try:
            main_account_mail = self._user_repository.get_first()
            if not main_account_mail or not main_account_mail.email:
                self._logger.error(
                    "Cannot send notification: No user found or user has no email"
                )
                return False

            result = self._email_sender.send_breach_notification(
                recipient_email=main_account_mail.email,
                breached_sites=new_breaches
            )

            return result

        except Exception as e:
            self._logger.error(f"Failed to send breach notification: {str(e)}")
            return False

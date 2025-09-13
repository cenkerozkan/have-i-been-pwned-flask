from typing import List, Optional, Set
from datetime import datetime
import time

from util.hibp_client import HibpClient
from repository.email_repository import EmailRepository
from repository.pwned_platform_repository import PwnedPlatformRepository
from service.notification_service import NotificationService
from db.model.email import Email
from db.model.pwned_platform import PwnedPlatform
from model.hibp_breached_site_model import HibpBreachedSiteModel
from util.logger import get_logger

class PwnChecker:
    def __init__(self) -> None:
        self._logger = get_logger(__name__)
        self._hibp_client = HibpClient()
        self._email_repository = EmailRepository()
        self._pwned_platform_repository = PwnedPlatformRepository()
        self._notification_service = NotificationService()
        self._rate_limit_wait_time: int = 120

    def _get_all_emails(self) -> List[Email]:
        return self._email_repository.get_all()
        
    def _check_email_for_breaches(self, email: Email) -> Optional[List[PwnedPlatform]]:
        try:
            breach_api_results: List[HibpBreachedSiteModel] = self._hibp_client.get_breached_accounts(email=email.email)
            self._logger.info(f"Breach api results: {breach_api_results}")
            if not breach_api_results:
                return None

            existing_breaches = set(self._pwned_platform_repository.get_by_email_id(email.id))
            self._logger.info(f"Existing breaches are: {existing_breaches}")
            
            breach_api_comparison = set()
            for breach in breach_api_results:

                added_date = breach.added_date
                if isinstance(added_date, str):
                    added_date = datetime.fromisoformat(added_date.replace("Z", "+00:00"))
                breach_date = breach.breach_date
                if isinstance(breach_date, str):
                    try:
                        breach_date = datetime.fromisoformat(breach_date.replace("Z", "+00:00")).date()
                    except Exception:
                        breach_date = datetime.strptime(breach_date, "%Y-%m-%d").date()
                breach_api_comparison.add(
                    PwnedPlatform(
                        name=breach.name,
                        title=breach.title,
                        domain=breach.domain,
                        breach_date=breach_date,
                        added_date=added_date,
                        description=breach.description,
                        is_verified=breach.is_verified,
                        data_classes=breach.data_classes
                    )
                )

            new_breaches: Set[PwnedPlatform] = breach_api_comparison - existing_breaches
            self._logger.info(f"Found {len(new_breaches)} new breaches!")
            return list(new_breaches)
        
        except Exception as e:
            self._logger.error(f"Error checking breaches for {email.email}: {str(e)}")
            return None
            
    def _save_breaches(self, email: Email, breaches: List[PwnedPlatform]) -> bool:
        try:
            if not breaches:
                return True
            
            for breach in breaches:
                breach.email_id = email.id
                
            result = self._pwned_platform_repository.insert_many(breaches)
            if result:
                self._logger.info(f"Saved {len(breaches)} new breaches for {email.email}")
            else:
                self._logger.error(f"Failed to save breaches for {email.email}")

            return result

        except Exception as e:
            self._logger.error(f"Error saving breaches for {email.email}: {str(e)}")
            return False
            
    def _send_notification(self, email: Email, breaches: List[HibpBreachedSiteModel]) -> bool:
        try:
            if not breaches:
                return True
                
            result = self._notification_service.send_breach_notification(
                email_address=email.email,
                new_breaches=breaches
            )
            
            if result:
                self._logger.info(f"Sent breach notification for {email.email}")
            else:
                self._logger.error(f"Failed to send breach notification for {email.email}")
                
            return result
            
        except Exception as e:
            self._logger.error(f"Error sending notification for {email.email}: {str(e)}")
            return False

    def run(self) -> None:
        self._logger.info("Starting breach check for all emails")
        emails: list[Email] = self._get_all_emails()
        
        for i, email in enumerate(emails):
            self._logger.info(f"Processing email {i+1}/{len(emails)}: {email.email}")
            
            new_breaches: Optional[List[PwnedPlatform]] = self._check_email_for_breaches(email)
            
            if new_breaches:
                save_result: bool = self._save_breaches(email, new_breaches)
                
                if save_result:
                    self._send_notification(email, new_breaches)
            
            if i < len(emails) - 1:
                self._logger.info(f"Waiting {self._rate_limit_wait_time} seconds before processing next email...")
                time.sleep(self._rate_limit_wait_time)
            
        self._logger.info("Completed breach check for all emails")
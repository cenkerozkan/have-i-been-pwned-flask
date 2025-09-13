from typing import List, Optional
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
        
    def _check_email_for_breaches(self, email: Email) -> Optional[List[HibpBreachedSiteModel]]:
        try:
            breach_results = self._hibp_client.get_breached_accounts(email=email.email)
            if not breach_results:
                return None
                
            existing_breaches = self._pwned_platform_repository.get_by_email_id(email.id)
            
            existing_breach_keys = {
                (breach.name, breach.added_date.isoformat() if breach.added_date else None) 
                for breach in existing_breaches
            }
            
            new_breaches: List[HibpBreachedSiteModel] = []
            for breach in breach_results:
                breach_key = (breach.name, breach.added_date.isoformat())
                if breach_key not in existing_breach_keys:
                    new_breaches.append(breach)
            
            if new_breaches:
                self._logger.info(f"Found {len(new_breaches)} new breaches for {email.email}")
                return new_breaches
            
            return None
                
        except Exception as e:
            self._logger.error(f"Error checking breaches for {email.email}: {str(e)}")
            return None
            
    def _save_breaches(self, email: Email, breaches: List[HibpBreachedSiteModel]) -> bool:
        try:
            if not breaches:
                return True
                
            pwned_platforms: List[PwnedPlatform] = []
            for breach in breaches:
                pwned_platform = PwnedPlatform(
                    name=breach.name,
                    title=breach.title,
                    domain=breach.domain,
                    breach_date=breach.breach_date,
                    added_date=breach.added_date,
                    description=breach.description,
                    is_verified=breach.is_verified,
                    email_id=email.id
                )
                pwned_platforms.append(pwned_platform)
                
            result = self._pwned_platform_repository.insert_many(pwned_platforms)
            if result:
                self._logger.info(f"Saved {len(pwned_platforms)} new breaches for {email.email}")
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
            
            new_breaches: Optional[List[HibpBreachedSiteModel]] = self._check_email_for_breaches(email)
            
            if new_breaches:
                save_result: bool = self._save_breaches(email, new_breaches)
                
                if save_result:
                    self._send_notification(email, new_breaches)
            
            if i < len(emails) - 1:
                self._logger.info(f"Waiting {self._rate_limit_wait_time} seconds before processing next email...")
                time.sleep(self._rate_limit_wait_time)
            
        self._logger.info("Completed breach check for all emails")
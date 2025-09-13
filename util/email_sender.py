import os
from typing import List, Optional, Dict, Any

from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask import Flask

from decorators.singleton import singleton
from util.logger import get_logger
from model.hibp_breached_site_model import HibpBreachedSiteModel

load_dotenv()

@singleton
class EmailSender:
    _logger = get_logger(__name__)
    _mail: Optional[Mail] = None

    def __init__(self) -> None:
        self._logger.debug("Initializing EmailSender")
        
    def init_app(self, app: Flask) -> None:
        app.config.update(
            MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True").lower() == "true",
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")
        )
        self._mail = Mail(app)
        self._logger.info("Email sender initialized with app context")

    def send_breach_notification(self, email_address: str, recipient_email: str, breached_sites: List[HibpBreachedSiteModel]) -> bool:
        """
        Send email notification about new breaches
        
        :param recipient_email: Email address to send notification to
        :param breached_sites: List of HibpBreachedSiteModel objects containing breach information
        :return: True if email sent successfully, False otherwise
        """
        if not self._mail:
            self._logger.error("Mail not initialized. Call init_app first.")
            return False
            
        try:
            subject: str = f"ALERT: New Security Breaches Detected"
            
            body: str = f"The following new breaches have been detected for {email_address}:\n\n"
            for site in breached_sites:
                body += f"- {site.title} ({site.breach_date}): {site.domain}\n"
                body += f"  Description: {site.description}\n"
                body += f"  Data compromised: {site.data_classes}\n\n"
            
            body += "\nPlease consider changing your passwords for these services."
            
            msg: Message = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body
            )
            
            self._mail.send(msg)
            self._logger.info(f"Breach notification sent to {recipient_email} for {email_address}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to send breach notification to {recipient_email} for {email_address}: {str(e)}")
            return False

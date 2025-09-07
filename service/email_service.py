from logging import Logger
from typing import Dict, List, Any
from sqlalchemy.exc import IntegrityError

from decorators.singleton import singleton
from repository.email_repository import EmailRepository
from repository.user_repository import UserRepository
from db.model.email import Email
from model.email_service_models import NewEmailModel
from util.logger import get_logger

@singleton
class EmailService:
    def __init__(self) -> None:
        self._db: EmailRepository = EmailRepository()
        self._user_repository: UserRepository = UserRepository()
        self._logger: Logger = get_logger(self.__class__.__name__)
    
    def get_all_emails(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            emails: List[Email] = self._db.get_all()
            
            result["success"] = True
            result["message"] = "Successfully retrieved all emails"
            result["data"] = {"emails": [{"id": email.id, "email": email.email} for email in emails]}
            
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to retrieve emails"
            result["error"] = str(e)
            self._logger.error(f"Failed to retrieve emails: {str(e)}")
        
        return result
    
    def delete_all_emails(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            deleted: bool = self._db.delete_all()
            
            if deleted:
                result["success"] = True
                result["message"] = f"Successfully deleted all emails"
            else:
                result["success"] = False
                result["message"] = "Failed to delete emails"
                
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to delete emails"
            result["error"] = str(e)
            self._logger.error(f"Failed to delete emails: {str(e)}")
        
        return result
    
    def create_email(self, new_email_data: NewEmailModel) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            user = self._user_repository.get_first()
            
            if not user:
                result["success"] = False
                result["message"] = "No user found to associate email with"
                return result
            
            email = Email(
                email=new_email_data.email,
                user_id=user.id
            )
            
            is_created: bool = self._db.insert_one(email)
            
            if is_created:
                result["success"] = True
                result["message"] = "Successfully added email"
                result["data"] = {"email": new_email_data.email}
            else:
                result["success"] = False
                result["message"] = "Failed to add email"
            
        except IntegrityError as e:
            result["success"] = False
            result["message"] = "Email already exists"
            result["error"] = str(e)
            self._logger.error(f"Email already exists: {str(e)}")
            
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to add email"
            result["error"] = str(e)
            self._logger.error(f"Failed to add email: {str(e)}")
        
        return result

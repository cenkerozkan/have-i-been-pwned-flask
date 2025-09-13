from logging import Logger
from typing import Dict, List, Any

from decorators.singleton import singleton
from repository.pwned_platform_repository import PwnedPlatformRepository
from db.model.pwned_platform import PwnedPlatform
from util.logger import get_logger


@singleton
class PwnedPlatformService:
    def __init__(self) -> None:
        self._db: PwnedPlatformRepository = PwnedPlatformRepository()
        self._logger: Logger = get_logger(self.__class__.__name__)

    def get_all_pwned_platforms(self) -> Dict[str, Any]:
        """Get all pwned platforms in the system"""
        result: Dict[str, Any] = {
            "success": False,
            "message": "",
            "data": {},
            "error": "",
        }

        try:
            platforms: List[PwnedPlatform] = self._db.get_all()

            # Convert to JSON format
            platforms_json = [platform.to_json() for platform in platforms]

            result["success"] = True
            result["message"] = "Successfully retrieved all pwned platforms"
            result["data"] = {"platforms": platforms_json}

        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to retrieve pwned platforms"
            result["error"] = str(e)
            self._logger.error(f"Failed to retrieve pwned platforms: {str(e)}")

        return result

    def delete_all_pwned_platforms(self) -> Dict[str, Any]:
        """Delete all pwned platforms in the system"""
        result: Dict[str, Any] = {
            "success": False,
            "message": "",
            "data": {},
            "error": "",
        }

        try:
            # Add delete_all method to repository if it doesn't exist
            if not hasattr(self._db, "delete_all"):
                # Implement delete_all directly in the service
                platforms = self._db.get_all()
                for platform in platforms:
                    self._db.delete_one(platform)
                deleted = True
            else:
                deleted = self._db.delete_all()

            if deleted:
                result["success"] = True
                result["message"] = "Successfully deleted all pwned platforms"
            else:
                result["success"] = False
                result["message"] = "Failed to delete pwned platforms"

        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to delete pwned platforms"
            result["error"] = str(e)
            self._logger.error(f"Failed to delete pwned platforms: {str(e)}")

        return result

    def get_by_email_id(self, email_id: int) -> Dict[str, Any]:
        """Get all pwned platforms for a specific email ID"""
        result: Dict[str, Any] = {
            "success": False,
            "message": "",
            "data": {},
            "error": "",
        }

        try:
            platforms: List[PwnedPlatform] = self._db.get_by_email_id(email_id)

            # Convert to JSON format
            platforms_json = [platform.to_json() for platform in platforms]

            result["success"] = True
            result["message"] = (
                f"Successfully retrieved pwned platforms for email ID {email_id}"
            )
            result["data"] = {"platforms": platforms_json}

        except Exception as e:
            result["success"] = False
            result["message"] = (
                f"Failed to retrieve pwned platforms for email ID {email_id}"
            )
            result["error"] = str(e)
            self._logger.error(
                f"Failed to retrieve pwned platforms for email ID {email_id}: {str(e)}"
            )

        return result

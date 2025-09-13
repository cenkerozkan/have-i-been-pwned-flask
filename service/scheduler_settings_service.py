from typing import Dict, List, Any, Union
from decorators.singleton import singleton
from util.logger import get_logger
from repository.scheduler_config_repository import SchedulerConfigRepository
from scheduler.scheduler import Scheduler

@singleton
class SchedulerSettingsService:
    def __init__(self) -> None:
        self._logger = get_logger(__name__)
        self._config_repo = SchedulerConfigRepository()
        self._scheduler = Scheduler()
        
    def get_pwn_check_settings(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            unit: str = self._config_repo.get_value("pwn_check_interval_unit", "hours")
            value: int = int(self._config_repo.get_value("pwn_check_interval_value", "1"))
            
            settings = {
                "interval_unit": unit,
                "interval_value": value
            }
            
            result["success"] = True
            result["message"] = "Scheduler settings retrieved successfully"
            result["data"] = settings
            
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to retrieve scheduler settings"
            result["error"] = str(e)
            
        return result
        
    def update_pwn_check_settings(self, interval_unit: str, interval_value: int) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            valid_units: List[str] = ["seconds", "minutes", "hours", "days"]
            if interval_unit not in valid_units:
                result["success"] = False
                result["message"] = f"Invalid interval unit"
                result["error"] = f"Interval unit must be one of: {', '.join(valid_units)}"
                return result
                
            if interval_value <= 0:
                result["success"] = False
                result["message"] = "Invalid interval value"
                result["error"] = "Interval value must be greater than 0"
                return result
                
            update_result: bool = self._scheduler.update_pwn_check_job(interval_unit, interval_value)
            
            if update_result:
                result["success"] = True
                result["message"] = "Scheduler settings updated successfully"
                self._logger.info(f"Updated pwn check settings: {interval_value} {interval_unit}")
            else:
                result["success"] = False
                result["message"] = "Failed to update scheduler settings"
                result["error"] = "Scheduler update operation failed"
                
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to update scheduler settings"
            result["error"] = str(e)
            
        return result
            
    def get_scheduler_status(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": False, "message": "", "data": {}, "error": ""}
        
        try:
            jobs = self._scheduler.get_jobs()
            
            result["success"] = True
            result["message"] = "Scheduler status retrieved successfully"
            result["data"] = {"jobs": jobs}
            
        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to retrieve scheduler status"
            result["error"] = str(e)
            
        return result
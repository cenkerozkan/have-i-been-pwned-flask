from typing import Dict, Optional, Any, Union
from decorators.singleton import singleton
from util.logger import get_logger
from db.db import db
from db.model.scheduler_config import SchedulerConfig

@singleton
class SchedulerConfigRepository:
    def __init__(self) -> None:
        self._logger = get_logger(__name__)
        
    def get_by_key(self, key: str) -> Optional[SchedulerConfig]:
        config: Optional[SchedulerConfig] = SchedulerConfig.query.filter_by(key=key).first()
        return config
        
    def get_value(self, key: str, default: Optional[str] = None) -> str:
        config: Optional[SchedulerConfig] = self.get_by_key(key)
        return config.value if config else default
        
    def set_value(self, key: str, value: str) -> bool:
        try:
            config: Optional[SchedulerConfig] = self.get_by_key(key)
            if config:
                config.value = value
                db.session.commit()
            else:
                config = SchedulerConfig(key=key, value=value)
                db.session.add(config)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.error(f"Failed to set config {key}: {str(e)}")
            return False
            
    def create_default_configs(self) -> None:
        defaults: Dict[str, str] = {
            "pwn_check_interval_unit": "hours",
            "pwn_check_interval_value": "1"
        }
        
        for key, value in defaults.items():
            if not self.get_by_key(key):
                self.set_value(key, value)
                self._logger.info(f"Created default config: {key}={value}")
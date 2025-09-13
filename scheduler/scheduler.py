from typing import Dict, List, Any, Optional, Callable
from flask import Flask
from flask_apscheduler import APScheduler
from decorators.singleton import singleton
from util.logger import get_logger
from repository.scheduler_config_repository import SchedulerConfigRepository


@singleton
class Scheduler:
    def __init__(self) -> None:
        self._logger = get_logger(__name__)
        self._scheduler = APScheduler()
        self._config_repo = SchedulerConfigRepository()
        self._app = None  # Store app reference

    def init_app(self, app: Flask) -> None:
        self._app = app  # Store app reference

        app.config.update(SCHEDULER_API_ENABLED=True, SCHEDULER_TIMEZONE="UTC")

        self._scheduler.init_app(app)
        with app.app_context():
            self._config_repo.create_default_configs()
        self._scheduler.start()
        self._register_jobs()

    def _register_jobs(self) -> None:
        self._register_pwn_check_job()

    def _register_pwn_check_job(self) -> None:
        from task.pwn_checker import PwnChecker

        interval_unit: str = self._config_repo.get_value(
            "pwn_check_interval_unit", "hours"
        )
        interval_value: int = int(
            self._config_repo.get_value("pwn_check_interval_value", "1")
        )

        interval_kwargs: Dict[str, int] = {interval_unit: interval_value}

        # Create a wrapper function that establishes app context using stored app reference
        def run_with_app_context():
            with self._app.app_context():
                PwnChecker().run()

        self._scheduler.add_job(
            id="pwn_check_job",
            func=run_with_app_context,
            trigger="interval",
            **interval_kwargs,
            name="Check for new breaches",
        )

        self._logger.info(
            f"Scheduled pwn check job to run every {interval_value} {interval_unit}"
        )

    def update_pwn_check_job(self, interval_unit: str, interval_value: int) -> bool:
        try:
            try:
                self._scheduler.remove_job("pwn_check_job")
            except Exception:
                pass

            self._config_repo.set_value("pwn_check_interval_unit", interval_unit)
            self._config_repo.set_value("pwn_check_interval_value", str(interval_value))

            self._register_pwn_check_job()

            return True
        except Exception as e:
            self._logger.error(f"Failed to update pwn check job: {str(e)}")
            return False

    def get_jobs(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat()
                if job.next_run_time
                else None,
                "trigger": str(job.trigger),
            }
            for job in self._scheduler.get_jobs()
        ]

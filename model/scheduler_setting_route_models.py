from pydantic import BaseModel


class SchedulerSettingsModel(BaseModel):
    interval_unit: str
    interval_value: int

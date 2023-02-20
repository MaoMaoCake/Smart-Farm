from pydantic import BaseModel
from typing import Optional
from datetime import time


class AutomationInput(BaseModel):
    ESP_id: int
    start_time: time
    end_time: Optional[time]
    automation_id: int
    hardware_type: str
    activate: Optional[bool]
    uv_percent: Optional[int]
    ir_percent: Optional[int]
    natural_percent: Optional[int]
    co2_threshold: Optional[int]
    humidity_threshold: Optional[int]
    temperature: Optional[int]


class DeleteAutomationInput(BaseModel):
    ESP_id: int
    automation_id: int
    hardware_type: str


class LightRequest(BaseModel):
    activate: bool
    uv_percent: int
    ir_percent: int
    natural_percent: int


class WateringRequest(BaseModel):
    activate: bool


class ACRequest(BaseModel):
    activate: bool
    temperature: int

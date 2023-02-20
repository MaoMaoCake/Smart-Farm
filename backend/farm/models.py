from pydantic import BaseModel
from typing import Optional
from datetime import time

class FarmOwner(BaseModel):
    id: int
    farmId: int
    userId: int


class FarmStats(BaseModel):
    farmId: int
    farmName: str
    temperature: int
    ACStatus: bool
    ACTemperature: int
    humidityLevel: int
    dehumidifierStatus: bool
    lightStatus: bool
    CO2Level: int
    CO2controllerStatus: bool

    def __init__(self,
                farm_id: int,
                farm_name: str,
                temperature: int,
                ac_status: bool,
                ac_temperature: int,
                humidity_level: int,
                dehumidifier_status: bool,
                light_status: bool,
                co2_level: int,
                co2_controller_status: bool
                ):
        super().__init__(
        farmId= farm_id,
        farmName = farm_name,
        temperature = temperature,
        ACStatus = ac_status,
        ACTemperature=ac_temperature,
        humidityLevel = humidity_level,
        dehumidifierStatus = dehumidifier_status,
        lightStatus = light_status,
        CO2Level = co2_level,
        CO2controllerStatus = co2_controller_status
        )


class Light(BaseModel):
    lightId: int
    lightName: str
    status: bool
    isAutomation: bool
    naturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int


class LightCombination(BaseModel):
    lightName: str
    presetId: int
    lightId: int
    naturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int

    def __init__(self,
                 light_name: str,
                preset_id: int,
                light_id: int,
                natural_lightDensity: int,
                UV_lightDensity: int,
                IR_lightDensity: int
                ):
        super().__init__(
            lightName=light_name,
            presetId=preset_id,
            lightId=light_id,
            naturalLightDensity=natural_lightDensity,
            UVLightDensity=UV_lightDensity,
            IRLightDensity=IR_lightDensity
        )


class FarmLightPreset(BaseModel):
    name: str
    preset_id: int


class LightStrength(BaseModel):
    lightId: int
    name: str
    automation: bool
    NaturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int


class AC(BaseModel):
    ACId: int
    ACName: str
    ACStatus: str

class CreateLightInput(BaseModel):
    name: Optional[str]
    automation: Optional[bool]
    NaturalLightDensity: Optional[int]
    UVLightDensity: Optional[int]
    IRLightDensity: Optional[int]


class UpdateLightStrengthInput(BaseModel):
    automation: bool
    NaturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int


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


class AutomationInputJSON(BaseModel):
    ESP_id: int
    start_time: str
    end_time: Optional[str]
    automation_id: int
    hardware_type: str
    activate: Optional[bool]
    uv_percent: Optional[int]
    ir_percent: Optional[int]
    natural_percent: Optional[int]
    co2_threshold: Optional[int]
    humidity_threshold: Optional[int]
    temperature: Optional[int]


class LightRequest(BaseModel):
    activate: bool
    uv_percent: int
    ir_percent: int
    natural_percent: int


class WateringRequest(BaseModel):
    activate: bool


class DehumidifierRequest(BaseModel):
    activate: bool


class ACRequest(BaseModel):
    activate: bool
    temperature: int


class ACAutomation(BaseModel):
    ACId: int
    temperature: int
    startTime: time
    endTime: Optional[time]


class DeleteAutomationInput(BaseModel):
    ESP_id: int
    automation_id: int
    hardware_type: str


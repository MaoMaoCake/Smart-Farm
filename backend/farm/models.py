from datetime import datetime, time

from pydantic import BaseModel
from typing import Optional
from datetime import time
from typing import List, Dict, Any

from .enum_list import ChangesType


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
    lightCombinationId: int
    lightName: str
    presetId: int
    lightId: int
    automation: bool
    naturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int

    def __init__(self,
                 light_combination_id: int,
                 light_name: str,
                 preset_id: int,
                 light_id: int,
                 automation: bool,
                 natural_lightDensity: int,
                 UV_lightDensity: int,
                 IR_lightDensity: int
                 ):
        super().__init__(
            lightCombinationId=light_combination_id,
            lightName=light_name,
            presetId=preset_id,
            lightId=light_id,
            automation=automation,
            naturalLightDensity=natural_lightDensity,
            UVLightDensity=UV_lightDensity,
            IRLightDensity=IR_lightDensity
        )


class UpdateLightCombination(BaseModel):
    lightName: str
    presetId: int
    lightId: int
    isAutomation: bool
    naturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int

    def __init__(self,
                 light_name: str,
                 preset_id: int,
                 light_id: int,
                 is_automation: bool,
                 natural_lightDensity: int,
                 UV_lightDensity: int,
                 IR_lightDensity: int
                 ):
        super().__init__(
            lightName=light_name,
            presetId=preset_id,
            lightId=light_id,
            isAutomation=is_automation,
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
    ACStatus: bool
    ACTemperature: Optional[int]


class Dehumidifier(BaseModel):
    DehumidifierId: int
    DehumidifierIsAvailable: str



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


class UpdateLightStrengthInputInPreset(BaseModel):
    automation: bool
    NaturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int


class LightAutomation(BaseModel):
    lightAutomationId: Optional[int]
    startTime: time
    endTime: time
    farmLightPresetId: int
    changes_type: Optional[ChangesType]
    
    
class AutomationInput(BaseModel):
    ESP_id: int
    start_time: time
    end_time: Optional[time]
    automation_id: int
    hardware_type: str
    activate: Optional[bool]
    light_combination_id: Optional[int]
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
    light_combination_id: Optional[int]
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
    light_combination_id: Optional[int]


class WateringRequest(BaseModel):
    activate: bool


class DehumidifierRequest(BaseModel):
    activate: bool


class ACRequest(BaseModel):
    activate: bool
    temperature: int


class SensorRequest(BaseModel):
    co2_threshold: Optional[int]
    humidity_threshold: Optional[int]
    temperature_threshold: Optional[int]


class ACAutomation(BaseModel):
    ACId: int
    temperature: int
    startTime: time
    endTime: Optional[time]


class FarmACAutomation(BaseModel):
    ACAutomationId: Optional[int]
    temperature: int
    startTime: time
    endTime: Optional[time]
    changes_type: Optional[ChangesType]


class DeleteAutomationInput(BaseModel):
    ESP_id: int
    automation_id: int
    hardware_type: str


class WateringAutomation(BaseModel):
    wateringAutomationId: Optional[int]
    wateringStartTime: time
    wateringEndTime: time
    changes_type: Optional[ChangesType]


class GetFarmSettings(BaseModel):
    MinCO2Level: int
    MaxHumidityLevel: int
    ACTemp: int
    isWateringAutomation: bool
    LightAutomations: List[LightAutomation]
    FarmLightPresets: List[FarmLightPreset]
    ACAutomations: List[FarmACAutomation]
    WateringAutomations: List[WateringAutomation]

    def __int__(self,
                min_co2_level: int,
                max_humidity: int,
                light_automations: List[LightAutomation],
                farm_light_presets: List[FarmLightPreset],
                ac_automations: List[FarmACAutomation],
                watering_automations: List[ WateringAutomation]
                ):
        super().__init__(
            MinCO2Level=min_co2_level,
            MaxHumidityLevel=max_humidity,
            LightAutomations=light_automations,
            FarmLightPresets=farm_light_presets,
            ACAutomations=ac_automations,
            WateringAutomations=watering_automations
        )


class FarmLightPresetUpdated(BaseModel):
    presetId: int
    farmId: int
    presetName: str


class UpdateFarmSettings(BaseModel):
    MinCO2Level: Optional[int]
    MaxHumidityLevel: Optional[int]
    LightAutomations: Optional[List[LightAutomation]]
    ACAutomations: Optional[List[FarmACAutomation]]
    WateringAutomations: Optional[List[WateringAutomation]]
    isWateringAutomation: bool


class CreateLightAutomationInput(BaseModel):
    startTime: time
    endTime: time
    farmLightPresetId: int
    username: str
    farmId: int
    farmId: int


class UpdateLightAutomationInput(BaseModel):
    automationId: int
    startTime: time
    endTime: time
    farmLightPresetId: int
    username: str


class CreateACAutomationInput(BaseModel):
    farmId: int
    startTime: time
    endTime: time
    temperature: int
    username: str


class UpdateACAutomationInput(BaseModel):
    automationId: int
    startTime: time
    endTime: time
    temperature: int
    username: str


class WaterController(BaseModel):
    waterControllerId: int
    automation: bool


class CreateWateringAutomationInput(BaseModel):
    farmId: int
    startTime: time
    endTime: time
    username: str


class UpdateWateringAutomationInput(BaseModel):
    automationId: int
    startTime: time
    endTime: time
    username: str


class GraphOutput(BaseModel):
    day: List[Dict[str, Any]]
    week: List[Dict[str, Any]]
    month: List[Dict[str, Any]]

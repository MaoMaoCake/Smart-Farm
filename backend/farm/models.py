from datetime import datetime, time

from pydantic import BaseModel
from typing import Optional, List


class FarmOwner(BaseModel):
    id: int
    farmId: int
    userId: int


class FarmStats(BaseModel):
    farmId: int
    farmName: str
    temperature: int
    ACStatus: bool
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
                 humidity_level: int,
                 dehumidifier_status: bool,
                 light_status: bool,
                 co2_level: int,
                 co2_controller_status: bool
                 ):
        super().__init__(
            farmId=farm_id,
            farmName=farm_name,
            temperature=temperature,
            ACStatus=ac_status,
            humidityLevel=humidity_level,
            dehumidifierStatus=dehumidifier_status,
            lightStatus=light_status,
            CO2Level=co2_level,
            CO2controllerStatus=co2_controller_status
        )


class Light(BaseModel):
    lightId: int
    lightName: str
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


class LightAutomation(BaseModel):
    lightAutomationId: int
    startTime: time
    endTime: time
    farmLightPresetId: int


class ACAutomation(BaseModel):
    ACAutomationId: int
    startTime: time
    endTime: time
    temperature: int


class WateringAutomation(BaseModel):
    wateringAutomationId: int
    wateringStartTime: time
    wateringEndTime: time


class GetFarmSettings(BaseModel):
    MinCO2Level: int
    MaxHumidityLevel: int
    LightAutomations: List[LightAutomation]
    FarmLightPresets: List[FarmLightPreset]
    ACAutomations: List[ACAutomation]
    WateringAutomations: List[WateringAutomation]

    def __int__(self,
                min_co2_level: int,
                max_humidity: int,
                light_automations: List[LightAutomation],
                farm_light_presets: List[FarmLightPreset],
                ac_automations: List[ACAutomation],
                watering_automations: List[WateringAutomation]
                ):
        super().__init__(
            MinCO2Level=min_co2_level,
            MaxHumidityLevel=max_humidity,
            LightAutomations=light_automations,
            FarmLightPresets=farm_light_presets,
            ACAutomations=ac_automations,
            WateringAutomations=watering_automations
        )

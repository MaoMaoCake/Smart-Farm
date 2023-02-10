from pydantic import BaseModel


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
        farmId= farm_id,
        farmName = farm_name,
        temperature = temperature,
        ACStatus = ac_status,
        humidityLevel = humidity_level,
        dehumidifierStatus = dehumidifier_status,
        lightStatus = light_status,
        CO2Level = co2_level,
        CO2controllerStatus = co2_controller_status
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


class AC(BaseModel):
    ACId: int
    ACName: str
    ACStatus: str

from pydantic import BaseModel

class FarmOwner(BaseModel):
    id: int
    farmId: int
    userId: int

class FarmStats(BaseModel):
    farmName: str
    temperature: int
    ACStatus: bool
    humidityLevel: int
    dehumidifierStatus: bool
    lightStatus: bool
    CO2Level: int
    CO2controllerStatus: bool

    def __init__(self,
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
    lightName: str
    isAutomation: bool
    naturalLightDensity: int
    UVLightDensity: int
    IRLightDensity: int


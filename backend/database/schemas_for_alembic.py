from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum, Boolean, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .utils import current_datetime
from .enum_list import Role

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    customData = Column(JSON, nullable=True)
    createAt = Column(DateTime, nullable=False, default=current_datetime())
    updateAt = Column(DateTime, nullable=False, default=current_datetime(), onupdate=current_datetime())
    deleteAt = Column(DateTime, nullable=True)
    createBy = Column(String, nullable=False)
    updateBy = Column(String, nullable=False)
    deleteBy = Column(String, nullable=True)


class UserDb(BaseModel):
    __tablename__ = "user"
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    verificationCode = Column(String, nullable=True)
    passwordChanging = Column(Boolean, nullable=False, default=False)
    changeCode = Column(String, nullable=True)


class FarmDb(BaseModel):
    __tablename__ = "farm"
    name = Column(String, nullable=False)
    maxHumidity = Column(Integer, nullable=False)
    minCO2 = Column(String, nullable=False)
    lightStatus = Column(Boolean, nullable=False)
    ACTemp =Column(Integer, nullable=False)
    farmKey = Column(String, nullable=False, unique=True)

    temperatureSensors = relationship("TemperatureSensorDB")
    ACs = relationship("ACDB")
    ACAutomations = relationship("ACAutomationDB")
    HumiditySensors = relationship("HumiditySensorDB")
    Dehumidifiers = relationship("DehumidifierDB")
    CO2Sensors = relationship("CO2SensorDB")
    CO2Controllers = relationship("CO2ControllerDB")
    wateringAutomations = relationship("WateringAutomationDB")
    Lights = relationship("LightDB")
    FarmLightPresets = relationship("FarmLightPresetDB")
    LightPresetAutomations = relationship("LightPresetAutomationDB")
    WaterController = relationship("WaterControllerDB")


class FarmOwnerDB(BaseModel):
    __tablename__ = "farmOwner"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)

    farm = relationship("FarmDb")
    user = relationship("UserDb")


class TemperatureSensorDB(BaseModel):
    __tablename__ = "temperatureSensor"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    temperature = Column(Integer, nullable=False)


class ACDB(BaseModel):
    __tablename__ = "AC"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    temperature = Column(Integer, nullable=False)
    fanLevel = Column(Integer, nullable=False)
    automation = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)


class ACAutomationDB(BaseModel):
    __tablename__ = "ACAutomation"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    temperature = Column(Integer, nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)


class HumiditySensorDB(BaseModel):
    __tablename__ = "humiditySensor"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    humidity = Column(Integer, nullable=False)


class DehumidifierDB(BaseModel):
    __tablename__ = "dehumidifier"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    status = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)


class CO2SensorDB(BaseModel):
    __tablename__ = "CO2Sensor"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    CO2 = Column(Integer, nullable=False)


class CO2ControllerDB(BaseModel):
    __tablename__ = "CO2Controller"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    status = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)


class WateringAutomationDB(BaseModel):
    __tablename__ = "wateringAutomation"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)


class LightAutomationDB(BaseModel):
    __tablename__ = "lightPresetAutomation"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    farmLightPresetId = Column(Integer, nullable=False)


class LightDB(BaseModel):
    __tablename__ = "light"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)
    automation = Column(Boolean, nullable=False)
    UVLightDensity = Column(Integer, nullable=False)
    IRLightDensity = Column(Integer, nullable=False)
    naturalLightDensity = Column(Integer, nullable=False)


class FarmLightPresetDB(BaseModel):
    __tablename__ = "farmLightPreset"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    name = Column(String, nullable=False)

    LightCombinations = relationship("LightCombinationDB")


class LightCombinationDB(BaseModel):
    __tablename__ = "lightCombination"
    lightId = Column(Integer, ForeignKey('light.id'), nullable=False)
    farmLightPresetId = Column(Integer, ForeignKey('farmLightPreset.id'), nullable=False)
    automation = Column(Boolean, nullable=False)
    UVLightDensity = Column(Integer, nullable=False)
    IRLightDensity = Column(Integer, nullable=False)
    naturalLightDensity = Column(Integer, nullable=False)

    Light = relationship("LightDB")


class LightPresetAutomationDB(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "lightPresetAutomation"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    farmLightPresetId = Column(Integer, ForeignKey('farmLightPreset.id'), nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)

    FarmLightPreset = relationship("FarmLightPresetDB")


class MQTTMapDB(BaseModel):
    __tablename__ = "MQTTMap"
    hardwareType = Column(Enum('LIGHT','AC','CO2_SENSOR','CO2_CONTROLLER','DEHUMIDIFIER','HUMIDITY_SENSOR',
                                          'TEMPERATURE_SENSOR','WATERING'), nullable=False)
    hardwareId = Column(Integer, nullable=False)
    ESPId = Column(Integer, ForeignKey('ESP.id'), nullable=False)
    ESPType = Column(Enum('SENSOR','CO2_CONTROLLER','LIGHT_CONTROLLER','AC_CONTROLLER',
                                     'DEHUMIDIFIER_CONTROLLER','WATERING_SYSTEM'), nullable=False)


class WaterControllerDB(BaseModel):
    __tablename__ = "waterController"
    farmId = Column(Integer, ForeignKey('farm.id'), nullable=False)
    status = Column(Boolean, nullable=False)
    automation = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)


class ESPsDB(BaseModel):
    __tablename__ = "ESP"
    isUsed = Column(Boolean, nullable=False)
    isAvailable = Column(Boolean, nullable=False)

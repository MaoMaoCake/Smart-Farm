import os

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from models import FarmOwner, FarmStats, Light, LightCombination, \
    FarmLightPreset, LightStrength, AC, CreateLightInput, \
    UpdateLightStrengthInput,UpdateAllSensorInput
from .schemas import MQTTMapDB, UserDb, FarmOwnerDB, FarmDb, TemperatureSensorDB, \
    ACDB, HumiditySensorDB, DehumidifierDB, CO2SensorDB, \
    CO2ControllerDB, LightDB, FarmLightPresetDB, LightCombinationDB

from .enum_list import HardwareType,ESPType

from dotenv import load_dotenv
load_dotenv('mqtt2db.env')

engine = create_engine(f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                       f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}")

Session = sessionmaker(bind=engine)
session = Session()

def update_light_strength_to_all_light(update_light_strength_input: UpdateLightStrengthInput,farm_id: int,username: str):
    print('asdf',update_light_strength_input)
    session.query(LightDB
        ).filter(LightDB.farmId == farm_id
            ).update({'UVLightDensity': update_light_strength_input.UVLightDensity,
                'IRLightDensity': update_light_strength_input.IRLightDensity,
                'naturalLightDensity': update_light_strength_input.NaturalLightDensity,
                'updateBy': username
                })
    session.commit()

    return

def update_dehumidifier_status(status: bool,
                                       farm_id: int,
                                       username: str):
    session.query(DehumidifierDB
                    ).filter(DehumidifierDB.farmId == farm_id
                    ).update({  'status': status,
                                'updateBy': username
                    })
    session.commit()

    return

def update_co2_controller_status(status: bool,
                                       farm_id: int,
                                       username: str):
    session.query(CO2ControllerDB
                    ).filter(CO2ControllerDB.farmId == farm_id
                    ).update({  'status': status,
                                'updateBy': username
                    })
    session.commit()

    return

def update_all_sensor_data(input: UpdateAllSensorInput,farm_id: int,username: str):
    session.query(CO2SensorDB
                    ).filter(CO2SensorDB.farmId == farm_id
                    ).update({  'CO2': input.CO2,
                                'updateBy': username
                    })
    session.query(HumiditySensorDB
                    ).filter(HumiditySensorDB.farmId == farm_id
                    ).update({  'humidity': input.humidity,
                                'updateBy': username
                    })
    session.query(TemperatureSensorDB
                    ).filter(TemperatureSensorDB.farmId == farm_id
                    ).update({  'temperature': input.temperature,
                                'updateBy': username
                    })
    session.commit()

    return

def get_farm_id_by_hardware_id(id: int, table: str) -> int:
    match table:
        case HardwareType.DEHUMIDIFIER.value:
            dehimidifier = session.query(DehumidifierDB).filter(DehumidifierDB.id == id).first()
            return dehimidifier.farmId
        case HardwareType.AC.value:
            ac = session.query(ACDB).filter(ACDB.id == id).first()
            return ac.farmId
        case HardwareType.LIGHT.value:
            light = session.query(LightDB).filter(LightDB.id == id).first()
            return light.farmId
        case HardwareType.CO2_SENSOR.value:
            co2 = session.query(CO2SensorDB).filter(CO2SensorDB.id == id).first()
            return co2.farmId
        case HardwareType.HUMIDITY_SENSOR.value:
            humidity_sensor = session.query(HumiditySensorDB).filter(HumiditySensorDB.id == id).first()
            return humidity_sensor.farmId
        case HardwareType.TEMPERATURE_SENSOR.value:
            temperature_sensor = session.query(TemperatureSensorDB).filter(TemperatureSensorDB.id == id).first() 
            return temperature_sensor.farmId
        case HardwareType.CO2_CONTROLLER.value:
            co2_emitter = session.query(CO2ControllerDB).filter(CO2ControllerDB.id == id).first() 
            return co2_emitter.farmId
        
def get_hardware_by_esp_id(esp_id: int):
    ESP_mapping = {}


    mqtt_map = session.query(MQTTMapDB).filter(MQTTMapDB.ESPId == esp_id).first()

    ESP_mapping["hardware_type"] = f"{mqtt_map.hardwareType.value}"
    ESP_mapping["hardware_id"] = mqtt_map.hardwareId

    return ESP_mapping

def get_threshold_by_farm_id(farm_id: int):
    threshold = {}

    farm = session.query(FarmDb).filter(FarmDb.id == farm_id).first()

    threshold["co2"] = farm.minCO2
    threshold["humidity"] = farm.maxHumidity

    return threshold

def get_ac_status_by_farm_id(farm_id: int):
    ac_status = {}

    AC = session.query(ACDB).filter(ACDB.farmId == farm_id).first()

    ac_status["temperature"] = AC.temperature
    ac_status["ac_status"] = AC.status

    return ac_status

def get_dehumidifier_esp_id_by_esp_id(esp_id: int) -> list[int]:
    espMap = session.query(MQTTMapDB).filter(MQTTMapDB.ESPId == esp_id,MQTTMapDB.ESPType == ESPType.DEHUMIDIFIER_CONTROLLER.value).all()

    return [espMap.ESPId for espMap in espMap]

def get_ac_esp_id_by_esp_id(esp_id: int) -> list[int]:
    espMap = session.query(MQTTMapDB).filter(MQTTMapDB.ESPId == esp_id,MQTTMapDB.ESPType == ESPType.AC_CONTROLLER.value).all()

    return [espMap.ESPId for espMap in espMap]

def get_co2_controller_esp_id_by_esp_id(esp_id: int) -> list[int]:
    espMap = session.query(MQTTMapDB).filter(MQTTMapDB.ESPId == esp_id,MQTTMapDB.ESPType == ESPType.CO2_CONTROLLER.value).all()

    return [espMap.ESPId for espMap in espMap]

def update_ac_status(status: bool,temperature: int,farm_id: int,username: str):
    session.query(ACDB
                    ).filter(ACDB.farmId == farm_id
                    ).update({  'status': status,
                                'temperature': temperature,
                                'updateBy': username
                    })
    session.commit()

    return




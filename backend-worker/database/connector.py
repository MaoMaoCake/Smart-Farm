import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worker.models import AutomationInput
from worker.enum_list import HardwareType

from .schemas import LightPresetAutomationDB,\
                     LightCombinationDB,\
                     LightDB,\
                     MQTTMapDB,\
                     ACAutomationDB,\
                     ACDB,\
                     WateringAutomationDB

engine = create_engine(f"{os.environ.get('DB_DIALECT')}://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
                       f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_DATABASE')}")

Session = sessionmaker(bind=engine)
session = Session()


def get_all_lights_automation() -> list[AutomationInput]:
    light_requests = []
    ESP_mapping = {}

    mqtt_map = session.query(MQTTMapDB).all()
    for mapping in mqtt_map:
        ESP_mapping[f"{mapping.hardwareType.value}{mapping.hardwareId}"] = mapping.ESPId

    light_automations = session.query(LightPresetAutomationDB).all()
    for light_automation in light_automations:
        light_settings = session.query(LightCombinationDB, LightDB)\
                                .join(LightDB, LightCombinationDB.lightId == LightDB.id)\
                                .filter(LightCombinationDB.farmLightPresetId == LightPresetAutomationDB.id)\
                                .all()

        for light_setting in light_settings:
            if light_setting.LightCombinationDB.automation:
                light_requests.append(AutomationInput(
                    ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light_setting.LightDB.id}"],
                    start_time=light_automation.startTime,
                    end_time=light_automation.endTime,
                    automation_id=light_automation.id,
                    hardware_type=HardwareType.LIGHT,
                    activate=True,
                    uv_percent=light_setting.LightCombinationDB.UVLightDensity,
                    ir_percent=light_setting.LightCombinationDB.IRLightDensity,
                    natural_percent=light_setting.LightCombinationDB.naturalLightDensity,
                ))

    return light_requests


def get_all_AC_automation() -> list[AutomationInput]:
    AC_requests = []
    ESP_mapping = {}

    mqtt_map = session.query(MQTTMapDB).all()
    for mapping in mqtt_map:
        ESP_mapping[f"{mapping.hardwareType.value}{mapping.hardwareId}"] = mapping.ESPId

    AC_automations = session.query(ACAutomationDB).all()
    for AC_automation in AC_automations:
        AC_settings = session.query(ACDB)\
                                .filter(ACDB.farmId == AC_automation.farmId)\
                                .all()

        for AC_setting in AC_settings:
            AC_requests.append(AutomationInput(
                ESP_id=ESP_mapping[f"{HardwareType.AC.value}{AC_setting.id}"],
                start_time=AC_automation.startTime,
                end_time=AC_automation.endTime,
                automation_id=AC_automation.id,
                hardware_type=HardwareType.AC,
                activate=True,
                temperature=AC_automation.temperature
            ))

    return AC_requests

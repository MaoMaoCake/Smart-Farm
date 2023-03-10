import os

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from auth.models import User
from farm.models import FarmOwner, FarmStats, Light, LightCombination, \
    FarmLightPreset, LightStrength, AC, CreateLightInput, \
    UpdateLightStrengthInput, GetFarmSettings, LightAutomation, FarmLightPreset, \
    ACAutomation, WateringAutomation, UpdateLightStrengthInputInPreset, UpdateLightCombination,\
    FarmACAutomation, FarmLightPreset, Dehumidifier, CreateLightAutomationInput,\
    UpdateLightAutomationInput, CreateACAutomationInput, UpdateACAutomationInput, WaterController,\
    CreateWateringAutomationInput, UpdateWateringAutomationInput
from .schemas import UserDb, FarmOwnerDB, FarmDb, TemperatureSensorDB, \
    ACDB, HumiditySensorDB, DehumidifierDB, CO2SensorDB, \
    CO2ControllerDB, LightDB, FarmLightPresetDB, LightCombinationDB, \
    ACAutomationDB, WateringAutomationDB, LightAutomationDB, MQTTMapDB, WaterControllerDB
from response.error_codes import get_http_exception
from response.response_dto import ResponseDto, get_response_status

engine = create_engine(f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                       f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}")

Session = sessionmaker(bind=engine)
session = Session()


def create_user(username: str, password_hashed: str, email: str, role: str, create_by: str) -> User:
    new_user = UserDb(username=username,
                      password=password_hashed,
                      email=email,
                      role=role,
                      createBy=create_by,
                      updateBy=create_by
                      )
    session.add(new_user)
    session.commit()

    return User(id=new_user.id, username=new_user.username, email=new_user.email, role=str(new_user.role.value))


def get_user_from_db(username: str) -> User | None:
    user = session.query(UserDb.id, UserDb.username, UserDb.role, UserDb.password).filter(
        UserDb.username == username).first()

    return User(id=user.id, username=user.username, password=user.password, role=str(user.role.value)) if user else None


def get_dup_email(email: str) -> User | None:
    user = session.query(UserDb.id, UserDb.username, UserDb.role, UserDb.password).filter(UserDb.email == email).first()

    return User(id=user.id, username=user.username, password=user.password, role=str(user.role.value)) if user else None


def add_farm_to_user_db(user: User, farm_id: str) -> FarmOwner | None:
    try:
        farm_owner = FarmOwnerDB(farmId=farm_id, userId=user.id, createBy=user.username, updateBy=user.username)
        session.add(farm_owner)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception("Database error occurred") from e

    return FarmOwner(id=farm_owner.id, farmId=farm_owner.farmId, userId=farm_owner.userId)


def check_farm_key_exist(farm_key: str) -> int | None:
    farm = session.query(FarmDb.id).filter(FarmDb.farmKey == farm_key).first()

    return farm.id if farm else None


def check_farm_owning(user_id: int, farm_id: int) -> int | None:
    farm_owning = session.query(FarmOwnerDB.id).filter(FarmOwnerDB.farmId == farm_id
                                                       , FarmOwnerDB.userId == user_id).first()

    return farm_owning.id if farm_owning else None


def check_ac_owning(farm_id: int, ac_id: int) -> int | None:
    ac_owning = session.query(ACDB).filter(ACDB.id == ac_id
                                            ,ACDB.farmId == farm_id).first()

    return ac_owning if ac_owning else None


def get_ac_automation(farm_id: int) -> [AC]:
    acs = session.query(ACAutomationDB).filter(ACAutomationDB.farmId == farm_id).all()

    return [ACAutomation(
        ACId=ac.id,
        temperature=ac.temperature,
        startTime=ac.startTime,
        endTime=ac.endTime
    ) for ac in acs]


def update_ac_automation_status(ac_id: int, turn_on: bool) -> AC:
    updated = session.query(ACDB).filter(ACDB.id == ac_id)\
                             .update({'automation': turn_on})
    session.commit()

    return updated


def list_farms_from_user_id(user_id: int) -> [FarmStats]:
    farm_owning = session.query(FarmOwnerDB.farmId).filter(FarmOwnerDB.userId == user_id).all()
    farm_ids = [farm[0] for farm in farm_owning]

    farms = session.query(FarmDb.id,
                          FarmDb.name,
                          TemperatureSensorDB.temperature,
                          ACDB.status,
                          HumiditySensorDB.humidity,
                          DehumidifierDB.status,
                          FarmDb.lightStatus,
                          CO2SensorDB.CO2,
                          CO2ControllerDB.status,
                          ).join(TemperatureSensorDB, FarmDb.id == TemperatureSensorDB.farmId
                                 ).join(ACDB, FarmDb.id == ACDB.farmId
                                        ).join(HumiditySensorDB, FarmDb.id == HumiditySensorDB.farmId
                                               ).join(DehumidifierDB, FarmDb.id == DehumidifierDB.farmId
                                                      ).join(CO2SensorDB, FarmDb.id == CO2SensorDB.farmId
                                                             ).join(CO2ControllerDB, FarmDb.id == CO2ControllerDB.farmId
                                                                    ).filter(FarmDb.id.in_(farm_ids)).all()

    return [FarmStats(*farm) for farm in farms]


def get_farm_stats_from_db(farm_id: int) -> FarmStats:
    farm = session.query(FarmDb.id,
                          FarmDb.name,
                          TemperatureSensorDB.temperature,
                          ACDB.status,
                          ACDB.temperature,
                          HumiditySensorDB.humidity,
                          DehumidifierDB.status,
                          FarmDb.lightStatus,
                          CO2SensorDB.CO2,
                          CO2ControllerDB.status,
                         ).join(TemperatureSensorDB, FarmDb.id == TemperatureSensorDB.farmId
                                ).join(ACDB, FarmDb.id == ACDB.farmId
                                       ).join(HumiditySensorDB, FarmDb.id == HumiditySensorDB.farmId
                                              ).join(DehumidifierDB, FarmDb.id == DehumidifierDB.farmId
                                                     ).join(CO2SensorDB, FarmDb.id == CO2SensorDB.farmId
                                                            ).join(CO2ControllerDB, FarmDb.id == CO2ControllerDB.farmId
                                                                   ).filter(FarmDb.id == farm_id).first()

    return FarmStats(*farm)


def check_farm_exist(farm_id: int) -> None:
    farm = session.query(FarmDb).filter(FarmDb.id == farm_id).first()
    if not farm:
        get_http_exception('FM404')
    return farm


def create_light(farm_id: int, create_light_input: CreateLightInput, username: str) -> Light:
    if not create_light_input.name:
        light_amount = len(get_lights_from_db(farm_id))
    try:
        new_light = LightDB(farmId=farm_id,
                            name=create_light_input.name if create_light_input.name else f'Light {light_amount}',
                            status=False,
                            isAvailable=True,
                            automation=create_light_input.automation if create_light_input.automation else True,
                            UVLightDensity=create_light_input.UVLightDensity if create_light_input.UVLightDensity else 50,
                            IRLightDensity=create_light_input.IRLightDensity if create_light_input.IRLightDensity else 50,
                            naturalLightDensity=create_light_input.NaturalLightDensity if create_light_input.NaturalLightDensity else 50,
                            createBy=username,
                            updateBy=username
                            )
        session.add(new_light)

        presets = get_light_presets_from_db(farm_id)
        light_combination_list = [LightCombinationDB(
            lightId=new_light.id,
            farmLightPresetId=preset.preset_id,
            automation=new_light.automation,
            UVLightDensity=new_light.UVLightDensity,
            IRLightDensity=new_light.IRLightDensity,
            naturalLightDensity=new_light.naturalLightDensity,
            createBy=username,
            updateBy=username
        ) for preset in presets]
        session.bulk_save_objects(light_combination_list)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')

    return Light(lightId=new_light.id,
                 lightName=new_light.name,
                 status=new_light.status,
                 isAutomation=new_light.automation,
                 UVLightDensity=new_light.UVLightDensity,
                 IRLightDensity=new_light.IRLightDensity,
                 naturalLightDensity=new_light.naturalLightDensity)


def get_lights_from_db(farm_id: int) -> [Light]:
    farm_lights = session.query(LightDB).filter(LightDB.farmId == farm_id).all()

    return [Light(lightId=light.id,
                    lightName=light.name,
                    status=light.status,
                    isAutomation=light.automation,
                    UVLightDensity=light.UVLightDensity,
                    IRLightDensity=light.IRLightDensity,
                    naturalLightDensity=light.naturalLightDensity)
              for light in farm_lights]


def get_lights_from_preset_db(preset_id: int) -> [LightCombination]:
    farm_lights = session.query(LightCombinationDB.id,
                                LightDB.name,
                                LightCombinationDB.farmLightPresetId,
                                LightCombinationDB.lightId,
                                LightCombinationDB.automation,
                                LightCombinationDB.UVLightDensity,
                                LightCombinationDB.IRLightDensity,
                                LightCombinationDB.naturalLightDensity). \
        join(LightCombinationDB, LightCombinationDB.lightId == LightDB.id) \
        .filter(LightCombinationDB.farmLightPresetId == preset_id).all()

    return [LightCombination(*light) for light in farm_lights]


def check_preset_exist(preset_id: int) -> None:
    preset = session.query(FarmLightPresetDB.id).filter(FarmLightPresetDB.id == preset_id).first()
    if not preset:
        get_http_exception('PS404')
    return None


def check_preset_owning(farm_id: int, preset_id: int) -> int | None:
    preset_owning = session.query(FarmLightPresetDB.id, FarmLightPresetDB.farmId).filter(
        FarmLightPresetDB.farmId == farm_id
        , FarmLightPresetDB.id == preset_id).first()

    return FarmLightPresetDB.id if preset_owning else None


def get_light_presets_from_db(farm_id: int) -> [FarmLightPreset]:
    farm_light_presets = session.query(FarmLightPresetDB).filter(FarmLightPresetDB.farmId == farm_id).all()

    return [FarmLightPreset(
        name=preset.name,
        preset_id=preset.id
    ) for preset in farm_light_presets]


def get_light_strength_from_db(light_id: int) -> LightStrength:
    light_strength_data = session.query(LightDB).filter(LightDB.id == light_id).first()

    return LightStrength(
        lightId=light_id,
        name=light_strength_data.name,
        automation=light_strength_data.automation,
        NaturalLightDensity=light_strength_data.naturalLightDensity,
        UVLightDensity=light_strength_data.UVLightDensity,
        IRLightDensity=light_strength_data.IRLightDensity
    )


def get_light_strength_in_preset_from_db(light_combination_id: int) -> LightStrength:
    light_strength_data = session.query(LightCombinationDB).filter(
        LightCombinationDB.id == light_combination_id).first()
    light_data = session.query(LightDB).filter(LightDB.id == light_strength_data.lightId).first()

    return LightStrength(
        lightId=light_strength_data.lightId,
        name=light_data.name,
        automation=light_strength_data.automation,
        NaturalLightDensity=light_strength_data.naturalLightDensity,
        UVLightDensity=light_strength_data.UVLightDensity,
        IRLightDensity=light_strength_data.IRLightDensity
    )


def check_light_combination_exist(combination_id) -> LightCombinationDB:
    light_combination = session.query(LightCombinationDB).filter(LightCombinationDB.id == combination_id).first()
    if not light_combination:
        get_http_exception('PC404')
    return light_combination


def check_light_combination_owning(light_combination_id: int, preset_id: int) -> int | None:
    preset_owning = session.query(LightCombinationDB.id, LightCombinationDB.farmLightPresetId).filter(
        LightCombinationDB.farmLightPresetId == preset_id
        , LightCombinationDB.id == light_combination_id).first()
    return LightCombinationDB.id if preset_owning else None


def check_light_owning(farm_id: int, preset_id: int) -> int | None:
    preset_owning = session.query(FarmLightPresetDB.id, FarmLightPresetDB.farmId).filter(
        FarmLightPresetDB.farmId == farm_id
        , FarmLightPresetDB.id == preset_id).first()

    return FarmLightPresetDB.id if preset_owning else None


def update_light_strength_to_all_light(update_light_strength_input: UpdateLightStrengthInput,
                                       farm_id: int,
                                       username: str) -> [Light]:
    session.query(LightDB
                  ).filter(LightDB.farmId == farm_id
                           ).update({'automation': update_light_strength_input.automation,
                                     'UVLightDensity': update_light_strength_input.UVLightDensity,
                                     'IRLightDensity': update_light_strength_input.IRLightDensity,
                                     'naturalLightDensity': update_light_strength_input.NaturalLightDensity,
                                     'updateBy': username
                                     })
    session.commit()

    return get_lights_from_db(farm_id)


def update_light_strength_in_db(update_light_strength_input: UpdateLightStrengthInput,
                                       light_id: int,
                                       username: str) -> Light:
    session.query(LightDB
                  ).filter(LightDB.id == light_id
                           ).update({'automation': update_light_strength_input.automation,
                                     'UVLightDensity': update_light_strength_input.UVLightDensity,
                                     'IRLightDensity': update_light_strength_input.IRLightDensity,
                                     'naturalLightDensity': update_light_strength_input.NaturalLightDensity,
                                     'updateBy': username
                                     })
    session.commit()

    light = session.query(LightDB).filter(LightDB.id == light_id).first()
    return Light(
        lightId=light.id,
        lightName=light.name,
        status=light.status,
        isAutomation=light.automation,
        UVLightDensity=light.UVLightDensity,
        IRLightDensity=light.IRLightDensity,
        naturalLightDensity=light.naturalLightDensity
        )


def update_light_strength_to_all_light_in_preset(
        update_light_strength_input_in_preset: UpdateLightStrengthInputInPreset,
        preset_id: int,
        username: str
        ) -> [LightCombination]:
    session.query(LightCombinationDB
                  ).filter(LightCombinationDB.farmLightPresetId == preset_id
                           ).update({'automation': update_light_strength_input_in_preset.automation,
                                     'UVLightDensity': update_light_strength_input_in_preset.UVLightDensity,
                                     'IRLightDensity': update_light_strength_input_in_preset.IRLightDensity,
                                     'naturalLightDensity': update_light_strength_input_in_preset.NaturalLightDensity,
                                     'updateBy': username
                                     })
    session.commit()

    return get_lights_from_preset_db(preset_id)


def update_light_combination_strength_in_db(update_light_strength_input: UpdateLightStrengthInput,
                                       light_combination_id: int,
                                       username: str) -> LightCombination:
    session.query(LightCombinationDB
                  ).filter(LightCombinationDB.id == light_combination_id
                           ).update({'automation': update_light_strength_input.automation,
                                     'UVLightDensity': update_light_strength_input.UVLightDensity,
                                     'IRLightDensity': update_light_strength_input.IRLightDensity,
                                     'naturalLightDensity': update_light_strength_input.NaturalLightDensity,
                                     'updateBy': username
                                     })
    session.commit()

    light = session.query(LightCombinationDB).filter(LightCombinationDB.id == light_combination_id).first()
    light_data = session.query(LightDB).filter(LightDB.id == light.lightId).first()
    return LightCombination(
        light_combination_id,
        light_data.name,
        light.farmLightPresetId,
        light.id,
        light.automation,
        light.UVLightDensity,
        light.IRLightDensity,
        light.naturalLightDensity
        )
def check_light_exist(light_id: int):
    light = session.query(LightDB).filter(LightDB.id == light_id).first()
    if not light:
        get_http_exception('LT404')
    return light


def check_light_exist_in_farm(farm_id: int, light_id: int):
    light = session.query(LightDB.farmId).filter(LightDB.farmId == farm_id, LightDB.id == light_id).first()
    if not light:
        get_http_exception('10')
    return None


def get_acs_from_db(farm_id: int) -> [AC]:
    acs = session.query(ACDB).filter(ACDB.farmId == farm_id).all()

    return [AC(
        ACId=ac.id,
        ACName=ac.name,
        ACStatus=ac.automation
    ) for ac in acs]


def get_dehumidifier_from_db(farm_id: int) -> [Dehumidifier]:
    dehumidifiers = session.query(DehumidifierDB).filter(DehumidifierDB.farmId == farm_id).all()

    return [Dehumidifier(
        DehumidifierId=dehumidifier.id,
        DehumidifierIsAvailable=dehumidifier.isAvailable
    ) for dehumidifier in dehumidifiers]


def create_preset(farm_id: int, username: str, default:bool=True) -> FarmLightPreset:
    preset_amount = len(get_light_presets_from_db(farm_id))
    try:
        new_preset = FarmLightPresetDB(farmId=farm_id,
                                       name=f'Preset {preset_amount + 1}',
                                       createBy=username,
                                       updateBy=username
                                       )
        session.add(new_preset)
        session.commit()

        lights = get_lights_from_db(farm_id)

        if default:
            light_combination_list = [LightCombinationDB(
                lightId=light.lightId,
                farmLightPresetId=new_preset.id,
                automation=True,
                UVLightDensity=50,
                IRLightDensity=50,
                naturalLightDensity=50,
                createBy=username,
                updateBy=username
            ) for light in lights]
            session.bulk_save_objects(light_combination_list)
            session.commit()
        else:
            light_combination_list = [LightCombinationDB(
                lightId=light.lightId,
                farmLightPresetId=new_preset.id,
                automation=light.isAutomation,
                UVLightDensity=light.UVLightDensity,
                IRLightDensity=light.IRLightDensity,
                naturalLightDensity=light.naturalLightDensity,
                createBy=username,
                updateBy=username
            ) for light in lights]

            session.bulk_save_objects(light_combination_list)
            session.commit()

        return FarmLightPreset(preset_id=new_preset.id, name=new_preset.name)
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')


def check_preset_in_light_automation_db(farm_id: int, preset_id: int):
    preset_automation = session.query(LightAutomationDB).filter(LightAutomationDB.farmId == farm_id,
                                                                LightAutomationDB.farmLightPresetId == preset_id).all()
    if preset_automation:
        get_http_exception('PA400')
    return preset_automation

def get_farm_setting_from_db(farm_id: int) -> GetFarmSettings:
    light_automations = session.query(LightAutomationDB).filter(LightAutomationDB.farmId == farm_id).all()
    farm_light_presets = session.query(FarmLightPresetDB).filter(FarmLightPresetDB.farmId == farm_id).all()
    ac_automations = session.query(ACAutomationDB).filter(ACAutomationDB.farmId == farm_id).all()
    watering_automations = session.query(WateringAutomationDB).filter(WateringAutomationDB.farmId == farm_id).all()
    farm_setting = session.query(FarmDb).filter(FarmDb.id == farm_id).first()
    water_controller = session.query(WaterControllerDB).filter(WaterControllerDB.farmId == farm_id).first()

    return GetFarmSettings(MinCO2Level=farm_setting.minCO2,
                           MaxHumidityLevel=farm_setting.maxHumidity,
                           ACTemp=farm_setting.ACTemp,
                           isWateringAutomation=water_controller.automation,
                           LightAutomations=[LightAutomation(
                               lightAutomationId=data.id,
                               startTime=data.startTime,
                               endTime=data.endTime,
                               farmLightPresetId=data.farmLightPresetId) for data in light_automations],
                           FarmLightPresets=[FarmLightPreset(
                               name=data.name,
                               preset_id=data.id
                           ) for data in farm_light_presets],
                           ACAutomations=[FarmACAutomation(
                               ACAutomationId=data.id,
                               startTime=data.startTime,
                               endTime=data.endTime,
                               temperature=data.temperature
                           ) for data in ac_automations],
                           WateringAutomations=[WateringAutomation(
                               wateringAutomationId=data.id,
                               wateringStartTime=data.startTime,
                               wateringEndTime=data.endTime
                           ) for data in watering_automations]
                           )


def delete_light_preset_in_db(preset_id: int) -> None:
    try:
        session.query(LightCombinationDB).filter(
            LightCombinationDB.farmLightPresetId == preset_id).delete(synchronize_session='fetch')
        session.commit()
        session.query(FarmLightPresetDB).filter(
            FarmLightPresetDB.id == preset_id).delete(synchronize_session='fetch')
        session.commit()
        return get_response_status('delete success')
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')


def get_esp_map(hardware_type: Optional[str]=None):
    ESP_mapping = {}

    if hardware_type:
        mqtt_map = session.query(MQTTMapDB).filter(MQTTMapDB.hardwareType==hardware_type).all()
    else:
        mqtt_map = session.query(MQTTMapDB).all()

    for mapping in mqtt_map:
        ESP_mapping[f"{mapping.hardwareType.value}{mapping.hardwareId}"] = mapping.ESPId

    return ESP_mapping


def check_preset_usage(preset_id: id) -> list[LightAutomation]:
    automations = session.query(LightAutomationDB).filter(LightAutomationDB.farmLightPresetId == preset_id).all()

    return [LightAutomation(
        lightAutomationId=automation.id,
        startTime=automation.startTime,
        endTime=automation.endTime,
        farmLightPresetId=automation.farmLightPresetId
    ) for automation in automations]


def update_farm_name(name: str, farm_id: int, username: str) -> FarmStats:
    session.query(FarmDb).filter(FarmDb.id == farm_id).update({'name': name, 'updateBy': username})
    session.commit()

    return get_farm_stats_from_db(farm_id)


def update_preset_name(name: str, preset_id: int, username: str) -> FarmLightPreset:
    session.query(FarmLightPresetDB).filter(FarmLightPresetDB.id == preset_id).update({'name': name, 'updateBy': username})
    session.commit()

    preset = session.query(FarmLightPresetDB).filter(FarmLightPresetDB.id == preset_id).first()
    return FarmLightPreset(
        presetId=preset_id,
        farmId=preset.farmId,
        presetName=preset.name
    )


def update_light_name(name: str, light_id: int, username: str) -> Light:
    session.query(LightDB).filter(LightDB.id == light_id).update({'name': name, 'updateBy': username})
    session.commit()

    light = session.query(LightDB).filter(LightDB.id == light_id).first()
    return Light(
        lightId=light.id,
        lightName=light.name,
        status=light.status,
        isAutomation=light.automation,
        UVLightDensity=light.UVLightDensity,
        IRLightDensity=light.IRLightDensity,
        naturalLightDensity=light.naturalLightDensity
    )


def update_AC_name(name: str, ac_id: int, username: str) -> AC:
    session.query(ACDB).filter(ACDB.id == ac_id).update({'name': name, 'updateBy': username})
    session.commit()

    ac = session.query(ACDB).filter(ACDB.id == ac_id).first()
    return AC(
        ACId=ac.id,
        ACName=ac.name,
        ACStatus=ac.automation
    )


def list_co2_sensors_id(farm_id: int) -> list[int]:
    co2_sensors = session.query(CO2SensorDB).filter(CO2SensorDB.farmId == farm_id).all()

    return [co2_sensor.id for co2_sensor in co2_sensors]


def list_humidity_sensors_id(farm_id: int) -> list[int]:
    humidity_sensors = session.query(HumiditySensorDB).filter(HumiditySensorDB.farmId == farm_id).all()

    return [humidity_sensor.id for humidity_sensor in humidity_sensors]


def delete_light_automation_in_db(automation_id: int) -> None:
    try:
        session.query(LightAutomationDB).filter(
            LightAutomationDB.id == automation_id).delete(synchronize_session='fetch')
        session.commit()
        return get_response_status('delete success')
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')


def create_light_automation_in_db(create_automation_input: CreateLightAutomationInput) -> LightAutomation:
    new_automation = LightAutomationDB(farmId=create_automation_input.farmId,
                      startTime=create_automation_input.startTime,
                      endTime=create_automation_input.endTime,
                      farmLightPresetId=create_automation_input.farmLightPresetId,
                      updateBy=create_automation_input.username,
                      createBy=create_automation_input.username
                      )
    session.add(new_automation)
    session.commit()

    return LightAutomation(
        lightAutomationId=new_automation.id,
        startTime=new_automation.startTime,
        endTime=new_automation.endTime,
        farmLightPresetId=new_automation.farmLightPresetId,
    )


def update_light_automation_in_db(update_automation_input: UpdateLightAutomationInput) -> None:
    session.query(LightAutomationDB
                  ).filter(LightAutomationDB.id == update_automation_input.automationId
                  ).update({
                    "startTime": update_automation_input.startTime,
                    "endTime": update_automation_input.endTime,
                    "farmLightPresetId": update_automation_input.farmLightPresetId,
                    "updateBy": update_automation_input.username
                  })
    session.commit()

def delete_ac_automation_in_db(automation_id: int) -> None:
    try:
        session.query(ACAutomationDB).filter(
            ACAutomationDB.id == automation_id).delete(synchronize_session='fetch')
        session.commit()
        return get_response_status('delete success')
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')


def create_ac_automation_in_db(create_automation_input: CreateACAutomationInput) -> FarmACAutomation:
    new_automation = ACAutomationDB(farmId=create_automation_input.farmId,
                      startTime=create_automation_input.startTime,
                      endTime=create_automation_input.endTime,
                      temperature=create_automation_input.temperature,
                      updateBy=create_automation_input.username,
                      createBy = create_automation_input.username
                      )
    session.add(new_automation)
    session.commit()

    return FarmACAutomation(
        ACAutomationId=new_automation.id,
        temperature=new_automation.temperature,
        startTime=new_automation.startTime,
        endTime=new_automation.endTime,
    )


def update_ac_automation_in_db(update_automation_input: UpdateACAutomationInput) -> None:
    session.query(ACAutomationDB
                  ).filter(ACAutomationDB.id == update_automation_input.automationId
                  ).update({
                    "startTime": update_automation_input.startTime,
                    "endTime": update_automation_input.endTime,
                    "temperature": update_automation_input.temperature,
                    "updateBy": update_automation_input.username
                  })
    session.commit()


def get_water_controller(farm_id: int) -> WaterController:
    water_controller = session.query(WaterControllerDB).filter(WaterControllerDB.farmId == farm_id).first()

    return WaterController(
        waterControllerId=water_controller.id,
        automation=water_controller.automation
    )


def update_water_controller(farm_id: int, automation: bool, username: str) -> WaterController:
    session.query(WaterControllerDB
                  ).filter(WaterControllerDB.farmId == farm_id
                  ).update(
                    {
                        "automation":automation,
                        "updateBy": username
                  })
    session.commit()


def delete_watering_automation_in_db(automation_id: int) -> None:
    try:
        session.query(WateringAutomationDB).filter(
            WateringAutomationDB.id == automation_id).delete(synchronize_session='fetch')
        session.commit()
        return get_response_status('delete success')
    except SQLAlchemyError as e:
        session.rollback()
        get_http_exception(error_code='03', message=f'Database error: {e}')


def create_watering_automation_in_db(create_automation_input: CreateWateringAutomationInput) -> WateringAutomation:
    new_automation = WateringAutomationDB(farmId=create_automation_input.farmId,
                      startTime=create_automation_input.startTime,
                      endTime=create_automation_input.endTime,
                      updateBy=create_automation_input.username,
                      createBy=create_automation_input.username
                      )
    session.add(new_automation)
    session.commit()

    return WateringAutomation(
        wateringAutomationId=new_automation.id,
        wateringStartTime=new_automation.startTime,
        wateringEndTime=new_automation.endTime,
    )


def update_watering_automation_in_db(update_automation_input: UpdateWateringAutomationInput) -> None:
    session.query(WateringAutomationDB
                  ).filter(WateringAutomationDB.id == update_automation_input.automationId
                  ).update({
                    "startTime": update_automation_input.startTime,
                    "endTime": update_automation_input.endTime,
                    "updateBy": update_automation_input.username,
                  })
    session.commit()
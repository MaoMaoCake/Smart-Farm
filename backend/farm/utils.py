import requests
import os
import json
from distutils.util import strtobool
from datetime import time, datetime


from database.connector import get_user_from_db, add_farm_to_user_db, \
    check_farm_key_exist, check_farm_owning, \
    list_farms_from_user_id, check_farm_exist,\
    get_lights_from_db, get_lights_from_preset_db, \
    check_preset_exist, check_preset_owning, \
    get_light_presets_from_db, get_light_strength_from_db, \
    check_light_exist_in_farm, check_light_exist,\
    get_acs_from_db, get_farm_stats_from_db, create_preset,\
    create_light, update_light_strength_to_all_light,\
    get_light_strength_in_preset_from_db, check_light_combination_exist,\
    check_light_combination_owning, delete_light_preset_in_db, get_farm_setting_from_db,\
    get_esp_map, check_ac_owning, get_ac_automation, update_ac_automation_status,\
    check_preset_usage, update_light_strength_in_db, update_light_combination_strength_in_db,\
    update_farm_name, update_preset_name, update_light_name, update_AC_name,\
    get_dehumidifier_from_db, list_co2_sensors_id, list_humidity_sensors_id,\
    create_light_automation_in_db, update_light_automation_in_db, delete_ac_automation_in_db,\
    create_ac_automation_in_db, update_ac_automation_in_db, get_water_controller,\
    delete_watering_automation_in_db, create_watering_automation_in_db,\
    update_watering_automation_in_db, update_light_strength_to_all_light_in_preset,\
    delete_light_automation_in_db, check_preset_in_light_automation_db, update_water_controller,\
    update_ac_temp_db, get_stats_from_mongo, get_all_user_from_db, get_all_farm_from_db, get_all_esp_from_db
    
from response.response_dto import ResponseDto, get_response_status
from response.error_codes import get_http_exception

from .config import create_mqtt_request

from .models import FarmOwner, FarmStats, Light,\
    LightCombination, FarmLightPreset, LightStrength,\
    CreateLightInput, UpdateLightStrengthInput, LightRequest,\
    AutomationInput, ACRequest, DeleteAutomationInput, AutomationInputJSON,\
    AC, ACAutomation, GetFarmSettings, UpdateLightStrengthInputInPreset,\
    Dehumidifier, DehumidifierRequest, UpdateFarmSettings, SensorRequest,\
    LightAutomation, CreateLightAutomationInput, UpdateLightAutomationInput,\
    UpdateACAutomationInput, CreateWateringAutomationInput, UpdateWateringAutomationInput,\
    CreateACAutomationInput, WateringAutomation

from .enum_list import HardwareType, ChangesType


def link_farm_to_user(username: str, farm_key: str) -> ResponseDto[FarmOwner]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    farm_id = check_farm_key_exist(farm_key)
    if not farm_id:
        get_http_exception('FK404')

    if check_farm_owning(user.id, farm_id):
        get_http_exception('FO001')

    farm_owner = add_farm_to_user_db(user, farm_id)

    return get_response_status(data=farm_owner)


def list_farms(username: str) -> ResponseDto[[FarmStats]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    farms = list_farms_from_user_id(user.id)

    return get_response_status(data=farms)


def get_farm_stats_from_farm_id(farm_id: int, username: str) -> ResponseDto[FarmStats]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_farm_stats_from_db(farm_id))


def create_new_light(farm_id: int, create_light_input: CreateLightInput, username: str) -> ResponseDto[Light]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=create_light(farm_id, create_light_input, username))


def list_light(farm_id: int, username: str) -> ResponseDto[[Light]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_lights_from_db(farm_id))


def get_light_in_preset(farm_id: int, preset_id: int, username: str) -> ResponseDto[[LightCombination]]:
    user = get_user_from_db(username)

    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    check_preset_exist(preset_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    return get_response_status(data=get_lights_from_preset_db(preset_id))


def create_new_preset(farm_id: int, username: str, is_default: bool) -> ResponseDto[FarmLightPreset]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=create_preset(farm_id, username, is_default))


def list_light_preset(farm_id: int, username: str) -> ResponseDto[[FarmLightPreset]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_light_presets_from_db(farm_id))


def get_light_strength_setting(light_id: int, farm_id: int, username: str) -> ResponseDto[LightStrength]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_light_exist(light_id)
    check_light_exist_in_farm(farm_id, light_id)

    return get_response_status(data=get_light_strength_from_db(light_id))


def get_light_strength_setting_in_preset(light_combination_id: int, preset_id, farm_id: int, username: str) -> ResponseDto[LightStrength]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_preset_exist(preset_id)
    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    check_light_combination_exist(light_combination_id)
    if not check_light_combination_owning(light_combination_id, preset_id):
        get_http_exception('10')
    return get_response_status(data=get_light_strength_in_preset_from_db(light_combination_id))


def list_acs(farm_id: int, username: str) -> ResponseDto[[AC]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_acs_from_db(farm_id))


def apply_light_strength_to_all_lights(updateLightStrengthInput: UpdateLightStrengthInput,
                                       farm_id: int,
                                       username: str) -> ResponseDto[[Light]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_light_density_limit(updateLightStrengthInput.NaturalLightDensity,
                              updateLightStrengthInput.UVLightDensity,
                              updateLightStrengthInput.IRLightDensity)

    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)
    lights = list_light(farm_id, username).data
    for light in lights:
        try:
            body = LightRequest(
               activate=light.status,
               uv_percent=updateLightStrengthInput.UVLightDensity,
               ir_percent= updateLightStrengthInput.IRLightDensity,
               natural_percent=updateLightStrengthInput.NaturalLightDensity
            )
            response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"]),
                                           message=json.dumps(body.__dict__))
            if response.status_code != 200:
                get_http_exception('03', message='MQTT connection failed')
        except:
            get_http_exception('03', message='MQTT connection failed')

    return get_response_status(data=update_light_strength_to_all_light(updateLightStrengthInput, farm_id, username))


def apply_light_strength_to_all_lights_in_preset(updateLightStrengthInputInPreset: UpdateLightStrengthInputInPreset,
                                       farm_id: int,
                                       preset_id: int,
                                       username: str) -> ResponseDto[[LightCombination]]:

    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_preset_exist(preset_id)

    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    check_light_density_limit(updateLightStrengthInputInPreset.NaturalLightDensity,
                              updateLightStrengthInputInPreset.UVLightDensity,
                              updateLightStrengthInputInPreset.IRLightDensity)

    automations = check_preset_usage(preset_id)
    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)
    lights = list_light(farm_id, username).data
    light_combinations = get_lights_from_preset_db(preset_id)
    automation_map = {}
    light_combination_map = {}

    for light_combination in light_combinations:
        automation_map[light_combination.lightId] = light_combination.automation
        light_combination_map[light_combination.lightId] = light_combination.lightCombinationId

    url = os.getenv("WORKER_SERVICE_URL")
    port = os.getenv("WORKER_SERVICE_PORT")
    path = f"{url}:{port}/task"

    if len(automations) > 0:
        for automation in automations:
            for light in lights:
                if light.isAutomation and automation_map[light.lightId]:
                    if check_automation_running(automation.startTime, automation.endTime):
                        try:
                            body = LightRequest(
                                       activate=True,
                                       uv_percent=updateLightStrengthInputInPreset.UVLightDensity,
                                       ir_percent=updateLightStrengthInputInPreset.IRLightDensity,
                                       natural_percent=updateLightStrengthInputInPreset.NaturalLightDensity,
                                       light_combination_id= light_combination_map[light.lightId]
                             )
                            response = create_mqtt_request(
                                topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"]),
                                   message=json.dumps(body.__dict__))
                            if response.status_code != 200:
                                get_http_exception('03', message='MQTT connection failed')
                        except:
                            get_http_exception('03', message='MQTT connection failed')

                    try:
                        body = AutomationInputJSON(
                            ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"],
                            start_time=str(automation.startTime),
                            end_time=str(automation.endTime),
                            automation_id=automation.lightAutomationId,
                            hardware_type=HardwareType.LIGHT,
                            activate=True,
                            light_combination_id=light_combination_map[light.lightId],
                            uv_percent=updateLightStrengthInputInPreset.UVLightDensity,
                            ir_percent=updateLightStrengthInputInPreset.IRLightDensity,
                            natural_percent=updateLightStrengthInputInPreset.NaturalLightDensity,
                        )
                        r: requests.Response = requests.put(url=path, data=json.dumps(body.__dict__))
                        if r.status_code != 200:
                            response_message = json.loads(r.content)
                            get_http_exception('03', message=str(response_message["message"]))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')
    # TODO check when integrate: possible bugs --> change to update only the one not turned on
    return get_response_status(data=update_light_strength_to_all_light_in_preset(updateLightStrengthInputInPreset, preset_id, username))


def check_light_density_limit(NaturalLightDensity: int,
                                UVLightDensity: int,
                                IRLightDensity: int):
    if NaturalLightDensity > 100 or NaturalLightDensity < 0:
        get_http_exception('LT401')
    if UVLightDensity > 100 or UVLightDensity < 0:
        get_http_exception('LT402')
    if IRLightDensity > 100 or IRLightDensity < 0:
        get_http_exception('LT403')


def delete_light_preset(farm_id: int, preset_id: int, username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_preset_exist(preset_id)
    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    check_preset_in_light_automation_db(farm_id, preset_id)

    return delete_light_preset_in_db(preset_id)


def light_controlling(farm_id: int, is_turn_on: bool, username: str):
    lights = list_light(farm_id, username).data
    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)
    for light in lights:
        if light.isAutomation:
            try:
                body = LightRequest(
                   activate=is_turn_on,
                   uv_percent=light.UVLightDensity,
                   ir_percent=light.IRLightDensity,
                   natural_percent=light.naturalLightDensity
                )
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"]),
                                               message=json.dumps(body.__dict__))
                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed')
            except:
                get_http_exception('03', message='MQTT connection failed')

    return get_response_status(message='Successfully send requests to mqtt broker')


def change_ac_temp(is_turn_on: bool, temperature: int, farm_id: int, username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    result = ac_controlling(farm_id, is_turn_on=is_turn_on, _temperature=temperature, username= username)

    if result.successful:
        update_ac_temp_db(farm_id, temperature)
        return get_response_status(message='Successfully send requests to mqtt broker and update database')
    else:
        get_http_exception('03', message='MQTT connection failed')


def ac_controlling(farm_id: int, is_turn_on: bool, _temperature: int ,username: str):
    acs = list_acs(farm_id, username).data
    ESP_mapping = get_esp_map(HardwareType.AC.value)
    for ac in acs:
        if ac.ACStatus:
            try:
                body = ACRequest(
                   activate=is_turn_on,
                   temperature=_temperature
                )
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.AC.value}{ac.ACId}"]),
                                               message=json.dumps(body.__dict__))

                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed!')
            except:
                get_http_exception('03', message='MQTT connection failed')

    return get_response_status(message='Successfully send requests to mqtt broker')


def update_ac_automation_by_id(ac_id: int, farm_id, is_turn_on: bool, username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    AC = check_ac_owning(farm_id, ac_id)
    if not AC:
        get_http_exception('10')

    if AC.automation and is_turn_on:
        get_http_exception(error_code='06', message='AC automation is already set to ON')
    elif not AC.automation and not is_turn_on:
        get_http_exception(error_code='06', message='AC automation is already set to OFF')

    AC_automations = get_ac_automation(farm_id)
    mapping = get_esp_map(HardwareType.AC)

    url = os.getenv("WORKER_SERVICE_URL")
    port = os.getenv("WORKER_SERVICE_PORT")
    path = f"{url}:{port}/task"

    if is_turn_on:
        create_ac_scheduler_task(AC_automations, mapping, ac_id, path)
        for AC_automation in AC_automations:
            if check_automation_running(AC_automation.startTime, AC_automation.endTime):
                try:
                    body = ACRequest(
                        activate=is_turn_on,
                        temperature=AC.temperature
                    )
                    response = create_mqtt_request(topic=str(mapping[f"{HardwareType.AC.value}{ac_id}"]),
                                                   message=json.dumps(body.__dict__))

                    if response.status_code != 200:
                        get_http_exception('03', message='MQTT connection failed')
                except:
                    create_ac_scheduler_task(AC_automations, mapping, ac_id, path)
                    get_http_exception('03', message='MQTT connection failed')

    elif not is_turn_on:
        delete_ac_scheduler_task(AC_automations, mapping, ac_id, path)
        try:
            body = ACRequest(
               activate=is_turn_on,
               temperature=AC.temperature
             )
            response = create_mqtt_request(topic=str(mapping[f"{HardwareType.AC.value}{ac_id}"]),
                                           message=json.dumps(body.__dict__))

            if response.status_code != 200:
                get_http_exception('03', message='MQTT connection failed')
        except:
            create_ac_scheduler_task(AC_automations, mapping, ac_id, path)
            get_http_exception('03', message='MQTT connection failed')

    return get_response_status(data=update_ac_automation_status(ac_id, is_turn_on))


def create_ac_scheduler_task(AC_automations: ACAutomation, mapping, ac_id: int, path: str):
    try:
        for AC_automation in AC_automations:
            body = AutomationInputJSON(
                ESP_id=mapping[f"{HardwareType.AC.value}{ac_id}"],
                start_time=str(AC_automation.startTime),
                end_time=str(AC_automation.endTime),
                automation_id=AC_automation.ACId,
                hardware_type=HardwareType.AC,
                activate=True,
                temperature=AC_automation.temperature
            )
            r: requests.Response = requests.post(url=path, data=json.dumps(body.__dict__))
            if r.status_code != 200:
                response_message = json.loads(r.content)
                get_http_exception('03', message=str(response_message["message"]))
    except:
        get_http_exception('03', message='Backend worker connection failed')


def delete_ac_scheduler_task(AC_automations: ACAutomation, mapping, ac_id: int, path: str):
    try:
        for AC_automation in AC_automations:
            body = DeleteAutomationInput(
                ESP_id=mapping[f"{HardwareType.AC.value}{ac_id}"],
                automation_id=AC_automation.ACId,
                hardware_type=HardwareType.AC.value
            )
            r = requests.delete(url=path, data=json.dumps(body.__dict__))
            if r.status_code != 200:
                response_message = json.loads(r.content)
                get_http_exception('03', message=str(response_message["message"]))
    except:
        get_http_exception('03', message='Backend worker connection failed')


def update_automation_to_all_acs(farm_id, is_turn_on: bool, username: str):
    acs = list_acs(farm_id, username).data

    for ac in acs:
        if (ac.ACStatus and not is_turn_on) or (not ac.ACStatus and is_turn_on):
            update_ac_automation_by_id(ac.ACId, farm_id, is_turn_on, username)

    return get_response_status(message='update successfully')
    

def get_farm_settings(farm_id, username: str) -> GetFarmSettings:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_farm_setting_from_db(farm_id))


def check_automation_running(start_time: time, end_time: time) -> bool:
    current_time = datetime.now().time()

    if (start_time < end_time) and (start_time <= current_time <= end_time):
        return True
    elif (end_time < start_time) and not (end_time <= current_time <= start_time):
        return True
    else:
        return False


def update_light_strength(update_input: UpdateLightStrengthInput,
                                        farm_id: int,
                                        light_id: int,
                                        username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    farm = check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    light = check_light_exist(light_id)
    check_light_exist_in_farm(farm_id, light_id)

    check_light_density_limit(update_input.NaturalLightDensity,
                              update_input.UVLightDensity,
                              update_input.IRLightDensity)

    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)

    is_on = farm.lightStatus and light.status and light.automation
    if is_on:
        try:
            body = LightRequest(
                    activate=True,
                    uv_percent=update_input.UVLightDensity,
                    ir_percent=update_input.IRLightDensity,
                    natural_percent=update_input.NaturalLightDensity,
                )
            response = create_mqtt_request(
                topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light_id}"]),
                message=json.dumps(body.__dict__))
            if response.status_code != 200:
                get_http_exception('03', message='MQTT connection failed')
        except:
            get_http_exception('03', message='MQTT connection failed')
        return get_response_status('Update has been sent to the device')
    else:
        updated_light = update_light_strength_in_db(update_input, light_id, username)
        return get_response_status(message='Light strength has been updated', data=updated_light)


def update_light_combination_strength(update_input: UpdateLightStrengthInput,
                                        farm_id: int,
                                        preset_id: int,
                                        light_combination_id: int,
                                        username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_preset_exist(preset_id)
    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    light_combination = check_light_combination_exist(light_combination_id)
    if not check_light_combination_owning(light_combination_id, preset_id):
        get_http_exception('10')

    light = check_light_exist(light_combination.lightId)

    check_light_density_limit(update_input.NaturalLightDensity,
                              update_input.UVLightDensity,
                              update_input.IRLightDensity)

    automations = check_preset_usage(preset_id)
    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)

    url = os.getenv("WORKER_SERVICE_URL")
    port = os.getenv("WORKER_SERVICE_PORT")
    path = f"{url}:{port}/task"

    if len(automations) > 0:
        for automation in automations:
            if light.automation and light_combination.automation:
                if check_automation_running(automation.startTime, automation.endTime):
                    try:
                        body = LightRequest(
                                activate=True,
                                uv_percent=update_input.UVLightDensity,
                                ir_percent=update_input.IRLightDensity,
                                natural_percent=update_input.NaturalLightDensity,
                                light_combination_id=light_combination.id
                            )
                        response = create_mqtt_request(
                            topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light_combination.lightId}"]),
                            message=json.dumps(body.__dict__))
                        if response.status_code != 200:
                            get_http_exception('03', message='MQTT connection failed')
                    except:
                        get_http_exception('03', message='MQTT connection failed')

                try:
                    body = AutomationInputJSON(
                        ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light.id}"],
                        start_time=str(automation.startTime),
                        end_time=str(automation.endTime),
                        automation_id=automation.lightAutomationId,
                        hardware_type=HardwareType.LIGHT,
                        activate=True,
                        light_combination_id=light_combination.id,
                        uv_percent=update_input.UVLightDensity,
                        ir_percent=update_input.IRLightDensity,
                        natural_percent=update_input.NaturalLightDensity,
                    )
                    r: requests.Response = requests.put(url=path, data=json.dumps(body.__dict__))
                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))
                except:
                    get_http_exception('03', message='Backend worker connection failed')

                if check_automation_running(automation.startTime, automation.endTime):
                    return get_response_status('Update has been sent to the device')

            updated_light = update_light_combination_strength_in_db(update_input, light_combination_id, username)
            return get_response_status(message='Light strength has been updated', data=updated_light)


def list_dehumidifier(farm_id: int, username: str) -> ResponseDto[[Dehumidifier]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_dehumidifier_from_db(farm_id))


def dehumidifier_controlling(farm_id: int, is_turn_on: bool, username: str):
    dehumidifiers = list_dehumidifier(farm_id, username).data
    ESP_mapping = get_esp_map(HardwareType.DEHUMIDIFIER.value)
    for dehumidifier in dehumidifiers:
        if dehumidifier.DehumidifierIsAvailable:
            try:
                body = DehumidifierRequest(activate=is_turn_on)
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.DEHUMIDIFIER.value}"
                                                                     f"{dehumidifier.DehumidifierId}"]),
                                               message=json.dumps(body.__dict__))
                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed!')
            except:
                get_http_exception('03', message='MQTT connection failed')

    return get_response_status(message='Successfully send requests to mqtt broker')


def update_farm_name_to_db(name: str, farm_id: int, username: str) -> ResponseDto:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=update_farm_name(name, farm_id, username))


def update_preset_name_to_db(name: str, farm_id: int, preset_id: int, username: str) -> ResponseDto:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_preset_exist(preset_id)
    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    return get_response_status(data=update_preset_name(name, preset_id, username))


def update_light_name_to_db(name: str, farm_id: int, light_id: int, username: str) -> ResponseDto:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    check_light_exist(light_id)
    check_light_exist_in_farm(farm_id, light_id)

    return get_response_status(data=update_light_name(name, light_id, username))


def update_AC_name_to_db(name: str, farm_id: int, ac_id: int, username: str) -> ResponseDto:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    AC = check_ac_owning(farm_id, ac_id)
    if not AC:
        get_http_exception('10')

    return get_response_status(data=update_AC_name(name, ac_id, username))


def are_periods_overlapping(automations: list[LightAutomation]):
    n = len(automations)
    for i in range(n):
        for j in range(i+1, n):
            start1 = automations[i].startTime
            end1 = automations[i].endTime
            start2 = automations[j].startTime
            end2 = automations[j].endTime
            if not (end1 <= start2 or end2 <= start1):
                return True
    return False


def are_watering_periods_overlapping(automations: list[WateringAutomation]):
    n = len(automations)
    without_duplication = set()

    for i in range(n):
        without_duplication.add(automations[i].wateringStartTime)
    if n == len(without_duplication):
        return False
    else:
        return True


def update_farm_setting_to_db(update_farm_input: UpdateFarmSettings, farm_id: int, username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    ESP_mapping = get_esp_map()
    url = os.getenv("WORKER_SERVICE_URL")
    port = os.getenv("WORKER_SERVICE_PORT")
    path = f"{url}:{port}/task"

    if update_farm_input.MinCO2Level:
        if 0 > update_farm_input.MinCO2Level:
            return get_http_exception(error_code='06', message="Minimum CO2 level cannot be lower then 0")
        co2_sensor_ids = list_co2_sensors_id(farm_id)
        for co2_sensor_id in co2_sensor_ids:
            try:
                body = SensorRequest(co2_threshold=update_farm_input.MinCO2Level)
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.CO2_SENSOR.value}"
                                                                     f"{co2_sensor_id}"]),
                                               message=json.dumps(body.__dict__))
                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed!')
            except:
                get_http_exception('03', message='MQTT connection failed')

    if update_farm_input.MaxHumidityLevel:
        if 100 < update_farm_input.MaxHumidityLevel:
            return get_http_exception(error_code='06', message="Maximum humidity level cannot be greater then 100")
        humidity_sensor_ids = list_humidity_sensors_id(farm_id)
        for humidity_sensor_id in humidity_sensor_ids:
            try:
                body = SensorRequest(humidity_threshold=update_farm_input.MaxHumidityLevel)
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.HUMIDITY_SENSOR.value}"
                                                                     f"{humidity_sensor_id}"]),
                                               message=json.dumps(body.__dict__))
                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed!')
            except:
                get_http_exception('03', message='MQTT connection failed')

    if update_farm_input.LightAutomations:
        delete_inputs = []
        update_inputs = []
        create_inputs = []
        no_changes_inputs = []
        for automation in update_farm_input.LightAutomations:
            match automation.changes_type:
                case ChangesType.DELETE.value:
                    delete_inputs.append(automation)
                case ChangesType.UPDATE.value:
                    update_inputs.append(automation)
                case ChangesType.CREATE.value:
                    create_inputs.append(automation)
                case ChangesType.NO_CHANGES.value | None:
                    no_changes_inputs.append(automation)

        for delete_input in delete_inputs:
            if check_automation_running(delete_input.startTime, delete_input.endTime):
                return get_http_exception('06', message="Cannot delete the ongoing automation")

        if are_periods_overlapping(update_inputs + create_inputs + no_changes_inputs):
            return get_http_exception('06', message='Light Automation Time overlapped')

        lights = list_light(farm_id, username).data
        light_automation_map = {}
        for light in lights:
            light_automation_map[light.lightId] = light.isAutomation

        for delete_input in delete_inputs:
            light_combinations = get_lights_from_preset_db(delete_input.farmLightPresetId)
            automation_map = {}

            for light_combination in light_combinations:
                automation_map[light_combination.lightId] = light_combination.automation

            for light in lights:
                if light.isAutomation and automation_map[light.lightId]:
                    try:
                        body = DeleteAutomationInput(
                            ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"],
                            automation_id=delete_input.lightAutomationId,
                            hardware_type=HardwareType.LIGHT,
                        )
                        r: requests.Response = requests.delete(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

            delete_light_automation_in_db(delete_input.lightAutomationId)

        for create_input in create_inputs:
            light_combinations = get_lights_from_preset_db(create_input.farmLightPresetId)

            new_automation = create_light_automation_in_db(CreateLightAutomationInput(
                farmId=farm_id,
                startTime=create_input.startTime,
                endTime=create_input.endTime,
                farmLightPresetId=create_input.farmLightPresetId,
                username=username
            ))

            for light_combination in light_combinations:
                if light_automation_map[light_combination.lightId] and light_combination.automation:
                    try:
                        body = AutomationInputJSON(
                            ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light_combination.lightId}"],
                            start_time=str(create_input.startTime),
                            end_time=str(create_input.endTime),
                            automation_id=new_automation.lightAutomationId,
                            hardware_type=HardwareType.LIGHT,
                            activate=True,
                            light_combination_id=light_combination.lightCombinationId,
                            uv_percent=light_combination.UVLightDensity,
                            ir_percent=light_combination.IRLightDensity,
                            natural_percent=light_combination.naturalLightDensity,
                        )
                        r: requests.Response = requests.post(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

        for update_input in update_inputs:
            light_combinations = get_lights_from_preset_db(update_input.farmLightPresetId)
            for light_combination in light_combinations:
                if light_automation_map[light_combination.lightId] and light_combination.automation:
                    try:
                        body = AutomationInputJSON(
                            ESP_id=ESP_mapping[f"{HardwareType.LIGHT.value}{light_combination.lightId}"],
                            start_time=str(update_input.startTime),
                            end_time=str(update_input.endTime),
                            automation_id=update_input.lightAutomationId,
                            hardware_type=HardwareType.LIGHT,
                            activate=True,
                            light_combination_id=light_combination.lightCombinationId,
                            uv_percent=light_combination.UVLightDensity,
                            ir_percent=light_combination.IRLightDensity,
                            natural_percent=light_combination.naturalLightDensity,
                        )
                        r: requests.Response = requests.put(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

            update_light_automation_in_db(UpdateLightAutomationInput(
                automationId=update_input.lightAutomationId,
                startTime=update_input.startTime,
                endTime=update_input.endTime,
                farmLightPresetId=update_input.farmLightPresetId,
                username=username
            ))

    if update_farm_input.ACAutomations:
        delete_inputs = []
        update_inputs = []
        create_inputs = []
        no_changes_inputs = []
        for automation in update_farm_input.ACAutomations:
            match automation.changes_type:
                case ChangesType.DELETE.value:
                    delete_inputs.append(automation)
                case ChangesType.UPDATE.value:
                    update_inputs.append(automation)
                case ChangesType.CREATE.value:
                    create_inputs.append(automation)
                case ChangesType.NO_CHANGES.value | None:
                    no_changes_inputs.append(automation)

        for delete_input in delete_inputs:
            if check_automation_running(delete_input.startTime, delete_input.endTime):
                return get_http_exception('06', message="Cannot delete the ongoing automation")

        if are_periods_overlapping(update_inputs + create_inputs + no_changes_inputs):
            return get_http_exception('06', message='AC Automation Time overlapped')

        acs = list_acs(farm_id, username).data

        for delete_input in delete_inputs:
            for ac in acs:
                if ac.ACStatus:
                    try:
                        body = DeleteAutomationInput(
                            ESP_id=ESP_mapping[f"{HardwareType.AC.value}{ac.ACId}"],
                            automation_id=delete_input.ACAutomationId,
                            hardware_type=HardwareType.AC,
                        )
                        r: requests.Response = requests.delete(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

            delete_ac_automation_in_db(delete_input.ACAutomationId)

        for create_input in create_inputs:
            new_automation = create_ac_automation_in_db(CreateACAutomationInput(
                farmId=farm_id,
                startTime=create_input.startTime,
                endTime=create_input.endTime,
                temperature=create_input.temperature,
                username=username
            ))
            for ac in acs:
                if ac.ACStatus:
                    try:
                        body = AutomationInputJSON(
                            ESP_id=ESP_mapping[f"{HardwareType.AC.value}{ac.ACId}"],
                            start_time=str(create_input.startTime),
                            end_time=str(create_input.endTime),
                            automation_id=new_automation.ACAutomationId,
                            hardware_type=HardwareType.AC,
                            activate=True,
                            temperature=create_input.temperature,
                        )
                        r: requests.Response = requests.post(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

        for update_input in update_inputs:
            for ac in acs:
                if ac.ACStatus:
                    try:
                        body = AutomationInputJSON(
                            ESP_id=ESP_mapping[f"{HardwareType.AC.value}{ac.ACId}"],
                            start_time=str(update_input.startTime),
                            end_time=str(update_input.endTime),
                            automation_id=update_input.ACAutomationId,
                            hardware_type=HardwareType.AC,
                            activate=True,
                            temperature=update_input.temperature,
                        )
                        r: requests.Response = requests.put(url=path, data=json.dumps(body.__dict__))
                    except:
                        get_http_exception('03', message='Backend worker connection failed')

                    if r.status_code != 200:
                        response_message = json.loads(r.content)
                        get_http_exception('03', message=str(response_message["message"]))

            update_ac_automation_in_db(UpdateACAutomationInput(
                automationId=update_input.ACAutomationId,
                startTime=update_input.startTime,
                endTime=update_input.endTime,
                temperature=update_input.temperature,
                username=username
            ))

    if update_farm_input.WateringAutomations:
        delete_inputs = []
        update_inputs = []
        create_inputs = []
        no_changes_inputs = []
        for automation in update_farm_input.WateringAutomations:
            match automation.changes_type:
                case ChangesType.DELETE.value:
                    delete_inputs.append(automation)
                case ChangesType.UPDATE.value:
                    update_inputs.append(automation)
                case ChangesType.CREATE.value:
                    create_inputs.append(automation)
                case ChangesType.NO_CHANGES.value | None:
                    no_changes_inputs.append(automation)

        # for delete_input in delete_inputs:
        #     if check_automation_running(delete_input.wateringStartTime, delete_input.wateringEndTime):
        #         return get_http_exception('06', message="Cannot delete the ongoing automation")

        if are_watering_periods_overlapping(update_inputs + create_inputs + no_changes_inputs):
            return get_http_exception('06', message='Watering Automation Time overlapped')

        water_controller = get_water_controller(farm_id)

        for delete_input in delete_inputs:
            if water_controller.automation:
                try:
                    body = DeleteAutomationInput(
                        ESP_id=ESP_mapping[f"{HardwareType.WATERING.value}{water_controller.waterControllerId}"],
                        automation_id=delete_input.wateringAutomationId,
                        hardware_type=HardwareType.WATERING,
                    )
                    r: requests.Response = requests.delete(url=path, data=json.dumps(body.__dict__))
                except:
                    get_http_exception('03', message='Backend worker connection failed')

                if r.status_code != 200:
                    response_message = json.loads(r.content)
                    get_http_exception('03', message=str(response_message["message"]))

            delete_watering_automation_in_db(delete_input.wateringAutomationId)

        for create_input in create_inputs:
            new_automation = create_watering_automation_in_db(CreateWateringAutomationInput(
                farmId=farm_id,
                startTime=create_input.wateringStartTime,
                endTime=create_input.wateringEndTime,
                username=username
            ))

            if update_farm_input.isWateringAutomation:
                try:
                    body = AutomationInputJSON(
                        ESP_id=ESP_mapping[f"{HardwareType.WATERING.value}{water_controller.waterControllerId}"],
                        start_time=str(create_input.wateringStartTime),
                        end_time=str(create_input.wateringEndTime),
                        automation_id=new_automation.wateringAutomationId,
                        hardware_type=HardwareType.WATERING,
                        activate=True,
                    )
                    r: requests.Response = requests.post(url=path, data=json.dumps(body.__dict__))
                except:
                    get_http_exception('03', message='Backend worker connection failed')

                if r.status_code != 200:
                    response_message = json.loads(r.content)
                    get_http_exception('03', message=str(response_message["message"]))

        for update_input in update_inputs + no_changes_inputs:
            try:
                body = AutomationInputJSON(
                    ESP_id=ESP_mapping[f"{HardwareType.WATERING.value}{water_controller.waterControllerId}"],
                    start_time=str(update_input.wateringStartTime),
                    end_time=str(update_input.wateringEndTime),
                    automation_id=update_input.wateringAutomationId,
                    hardware_type=HardwareType.WATERING,
                    activate=True,
                )
                if update_farm_input.isWateringAutomation and water_controller.automation:
                    r: requests.Response = requests.put(url=path, data=json.dumps(body.__dict__))
                elif update_farm_input.isWateringAutomation and not water_controller.automation:
                    r: requests.Response = requests.post(url=path, data=json.dumps(body.__dict__))
                elif not update_farm_input.isWateringAutomation and water_controller.automation:
                    delete_body = DeleteAutomationInput(
                        ESP_id=ESP_mapping[f"{HardwareType.WATERING.value}{water_controller.waterControllerId}"],
                        automation_id=update_input.wateringAutomationId,
                        hardware_type=HardwareType.WATERING,
                    )
                    r: requests.Response = requests.delete(url=path, data=json.dumps(delete_body.__dict__))
                else:
                    r = requests.Response
                    r.status_code = 200
            except:
                get_http_exception('03', message=f'Backend worker connection failed')

            if r.status_code != 200:
                response_message = json.loads(r.content)
                print(response_message)
                get_http_exception('03', message=str(response_message["message"]))

            update_watering_automation_in_db(UpdateWateringAutomationInput(
                automationId=update_input.wateringAutomationId,
                startTime=update_input.wateringStartTime,
                endTime=update_input.wateringEndTime,
                username=username
            ))

        if water_controller.automation != update_farm_input.isWateringAutomation:
            update_water_controller(farm_id, update_farm_input.isWateringAutomation, username)

    return get_response_status('Update has been sent to devices')


def get_stats_graph(farm_id: int, username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_stats_from_mongo(farm_id))


def list_users(username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    return get_response_status(data=get_all_user_from_db())

def list_farms_by_admin(username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    return get_response_status(data=get_all_farm_from_db())


def list_ESPs_by_admin(username: str):
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    return get_response_status(data=get_all_esp_from_db())
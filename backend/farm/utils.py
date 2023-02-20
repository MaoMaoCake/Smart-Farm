import requests
import os
import json
from distutils.util import strtobool

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
    check_light_combination_owning, delete_light_preset_in_db,\
    get_esp_map, check_ac_owning, get_ac_automation, update_ac_automation_status
from response.response_dto import ResponseDto, get_response_status
from response.error_codes import get_http_exception

from .config import create_mqtt_request

from .models import FarmOwner, FarmStats, Light,\
    LightCombination, FarmLightPreset, LightStrength,\
    CreateLightInput, UpdateLightStrengthInput, LightRequest,\
    AutomationInput, ACRequest, DeleteAutomationInput, AutomationInputJSON,\
    AC, ACAutomation

from .enum_list import HardwareType


def link_farm_to_user(username: str, farm_key: str) -> ResponseDto[FarmOwner]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    farm_id = check_farm_key_exist(farm_key)
    if not farm_id:
        get_http_exception('FM404')

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
        print(light)
        try:
            response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"]),
                                           message=str(LightRequest(
                                               activate=light.status,
                                               uv_percent=updateLightStrengthInput.UVLightDensity,
                                               ir_percent= updateLightStrengthInput.IRLightDensity,
                                               natural_percent=updateLightStrengthInput.NaturalLightDensity
                                           )))
            if response.status_code != 200:
                get_http_exception('03', message='MQTT connection failed')
        except:
            get_http_exception('03', message='MQTT connection failed')

    return get_response_status(data=update_light_strength_to_all_light(updateLightStrengthInput, farm_id, username))


def check_light_density_limit( NaturalLightDensity: int,
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

    return delete_light_preset_in_db(preset_id)


def light_controlling(farm_id: int, is_turn_on: bool, username: str):
    lights = list_light(farm_id, username).data
    ESP_mapping = get_esp_map(HardwareType.LIGHT.value)
    for light in lights:
        if light.isAutomation:
            try:
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.LIGHT.value}{light.lightId}"]),
                                               message=str(LightRequest(
                                                   activate=is_turn_on,
                                                   uv_percent=light.UVLightDensity,
                                                   ir_percent=light.IRLightDensity,
                                                   natural_percent=light.naturalLightDensity
                                               )))
                if response.status_code != 200:
                    get_http_exception('03', message='MQTT connection failed')
            except:
                get_http_exception('03', message='MQTT connection failed')

    return get_response_status(message='Successfully send requests to mqtt broker')


def ac_controlling(farm_id: int, is_turn_on: bool, _temperature: int ,username: str):
    acs = list_acs(farm_id, username).data
    ESP_mapping = get_esp_map(HardwareType.AC.value)
    for ac in acs:
        if ac.ACStatus:
            try:
                response = create_mqtt_request(topic=str(ESP_mapping[f"{HardwareType.AC.value}{ac.ACId}"]),
                                               message=str(ACRequest(
                                                   activate=is_turn_on,
                                                   temperature=_temperature
                                               )))

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
    elif not is_turn_on:
        delete_ac_scheduler_task(AC_automations, mapping, ac_id, path)
        try:
            response = create_mqtt_request(topic=str(mapping[f"{HardwareType.AC.value}{ac_id}"]),
                                           message=str(ACRequest(
                                               activate=is_turn_on,
                                               temperature=AC.temperature
                                           )))

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
        if (bool(strtobool(ac.ACStatus)) and not is_turn_on) or (not bool(strtobool(ac.ACStatus)) and is_turn_on):
            update_ac_automation_by_id(ac.ACId, farm_id, is_turn_on, username)

    return get_response_status(message='update successfully')

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
    get_esp_map
from response.response_dto import ResponseDto, get_response_status
from response.error_codes import get_http_exception

from .config import create_mqtt_request

from .models import FarmOwner, FarmStats, Light,\
    LightCombination, FarmLightPreset, LightStrength,\
    CreateLightInput, UpdateLightStrengthInput, LightRequest

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


def list_acs(farm_id: int, username: str) -> ResponseDto[[FarmStats]]:
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

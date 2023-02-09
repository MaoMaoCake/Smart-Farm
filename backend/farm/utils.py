from database.connector import get_user_from_db, add_farm_to_user_db, check_farm_key_exist, check_farm_owning, list_farms_from_user_id, check_farm_exist,get_lights_from_db, get_lights_from_preset_db, check_preset_exist, check_preset_owning
from response.response_dto import ResponseDto, get_response_status
from response.error_codes import get_http_exception

from .models import FarmOwner, FarmStats, Light, FarmLightPreset


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


def list_light(farm_id: int, username: str) -> ResponseDto[[Light]]:
    user = get_user_from_db(username)
    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_lights_from_db(farm_id))


def get_light_in_preset(farm_id: int, preset_id: int, username: str) -> ResponseDto[[Light]]:
    user = get_user_from_db(username)

    if not user:
        get_http_exception('US404')

    check_farm_exist(farm_id)

    check_preset_exist(preset_id)

    if not check_preset_owning(farm_id, preset_id):
        get_http_exception('10')

    if not check_farm_owning(user.id, farm_id):
        get_http_exception('10')

    return get_response_status(data=get_lights_from_preset_db(preset_id))


# def list_light_preset(farm_id: int, username: str) -> ResponseDto[[FarmLightPreset]]:
#     user = get_user_from_db(username)
#     if not user:
#         get_http_exception('US404')
#
#     check_farm_exist(farm_id)
#
#     if not check_farm_owning(user.id, farm_id):
#         get_http_exception('10')
#
#     return get_response_status(data=get_lights_from_db(farm_id))



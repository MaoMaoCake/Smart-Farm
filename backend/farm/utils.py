from database.connector import get_user_from_db, add_farm_to_user_db, check_farm_key_exist, check_farm_owning
from response.response_dto import ResponseDto, get_response_status
from response.error_codes import get_http_exception

from .models import FarmOwner

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





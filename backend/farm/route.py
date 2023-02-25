from fastapi import APIRouter, Depends

# OAuth Libraries
from auth.utils import get_current_active_user
from response.response_dto import ResponseDto

from auth.models import User
from .utils import link_farm_to_user, list_farms,\
    list_light, get_light_in_preset, list_light_preset,\
    list_acs, get_farm_stats_from_farm_id, get_light_strength_setting,\
    create_new_preset, create_new_light, apply_light_strength_to_all_lights,\
    get_light_strength_setting_in_preset, get_farm_settings, delete_light_preset, \
    apply_light_strength_to_all_lights_in_preset, light_controlling,\
    update_ac_automation_by_id, ac_controlling, update_automation_to_all_acs,\
    update_light_strength, update_light_combination_strength,update_farm_name_to_db,\
    update_preset_name_to_db, update_light_name_to_db, update_AC_name_to_db,\
    dehumidifier_controlling

from .models import FarmOwner, FarmStats, Light, LightCombination,\
    FarmLightPreset, AC, LightStrength, CreateLightInput, \
    UpdateLightStrengthInput, GetFarmSettings, UpdateLightStrengthInputInPreset

farmRouter = APIRouter()


@farmRouter.post("/add", response_model=ResponseDto[FarmOwner], tags=["Farm"])
async def add_farm_to_user(farm_key: str, current_user: User = Depends(get_current_active_user)):

    return link_farm_to_user(current_user.username, farm_key)


@farmRouter.get("/list", response_model=ResponseDto[FarmStats], tags=["Farm"])
async def list_all_farms(current_user: User = Depends(get_current_active_user)):

    return list_farms(current_user.username)


@farmRouter.get("/farm/{farm_id}/stats", response_model=ResponseDto[FarmStats], tags=["Farm"])
async def get_farm_stats(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return get_farm_stats_from_farm_id(farm_id, current_user.username)


@farmRouter.post("/farm/{farm_id}/light/create", response_model=ResponseDto[Light], tags=["Farm"])
async def create_light(farm_id: int, create_light_input: CreateLightInput, current_user: User = Depends(get_current_active_user)):

    return create_new_light(farm_id, create_light_input, current_user.username)


@farmRouter.get("/farm/{farm_id}/light/list", response_model=ResponseDto[Light], tags=["Farm"])
async def list_all_lights(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_light(farm_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/light/preset/{preset_id}", response_model=ResponseDto[LightCombination], tags=["Farm"])
async def show_light_from_preset(farm_id: int, preset_id: int, current_user: User = Depends(get_current_active_user)):

    return get_light_in_preset(farm_id, preset_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/light/preset", response_model=ResponseDto[FarmLightPreset], tags=["Farm"])
async def list_all_light_preset(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_light_preset(farm_id, current_user.username)


@farmRouter.post("/farm/{farm_id}/light/preset/create_from_current", response_model=ResponseDto[FarmLightPreset], tags=["Farm"])
async def create_preset(farm_id: int, is_current_setting:bool, current_user: User = Depends(get_current_active_user)):

    return create_new_preset(farm_id, current_user.username, not is_current_setting)


@farmRouter.get("/farm/{farm_id}/AC/list/", response_model=ResponseDto[AC], tags=["Farm"])
async def list_all_acs(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_acs(farm_id, current_user.username)
    
    
@farmRouter.get("/farm/{farm_id}/light/{light_id}}", response_model=ResponseDto[LightStrength], tags=["Farm"])
async def get_light_strength(light_id: int, farm_id: int, current_user: User = Depends(get_current_active_user)):

    return get_light_strength_setting(light_id, farm_id, current_user.username)


@farmRouter.patch("/farm/{farm_id}/light/{light_id}/update_all}", response_model=ResponseDto[Light], tags=["Farm"])
async def apply_light_strength_to_all(updateLightStrengthInput: UpdateLightStrengthInput,
                                      farm_id: int,
                                      current_user: User = Depends(get_current_active_user)):

    return apply_light_strength_to_all_lights(updateLightStrengthInput, farm_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/{preset_id}/{light_combination_id}}", response_model=ResponseDto[LightStrength], tags=["Farm"])
async def get_light_strength_in_preset(light_combination_id: int, preset_id: int, farm_id: int, current_user: User = Depends(get_current_active_user)):

    return get_light_strength_setting_in_preset(light_combination_id, preset_id, farm_id, current_user.username)


@farmRouter.get("/farm/{farm_id}", response_model=ResponseDto[GetFarmSettings], tags=["Farm"])
async def get_farm_setting(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return get_farm_settings(farm_id, current_user.username)


@farmRouter.delete("/farm/{farm_id}/{preset_id}}", response_model=ResponseDto, tags=["Farm"])
async def delete_preset(farm_id: int, preset_id: int, current_user: User = Depends(get_current_active_user)):

    return delete_light_preset(farm_id, preset_id, current_user.username)


@farmRouter.post("/farm/{farm_id}/light/control}", response_model=ResponseDto, tags=["Farm"])
async def control_light(farm_id: int, is_turn_on: bool, current_user: User = Depends(get_current_active_user)):

    return light_controlling(farm_id, is_turn_on, current_user.username)


@farmRouter.post("/farm/{farm_id}/ac/control}", response_model=ResponseDto, tags=["Farm"])
async def control_ac(farm_id: int, is_turn_on: bool, temperature: int ,current_user: User = Depends(get_current_active_user)):

    return ac_controlling(farm_id, is_turn_on, temperature ,current_user.username)


@farmRouter.post("/farm/{farm_id}/dehumidifier/control}", response_model=ResponseDto, tags=["Farm"])
async def control_dehumidifier(farm_id: int, is_turn_on: bool, current_user: User = Depends(get_current_active_user)):

    return dehumidifier_controlling(farm_id, is_turn_on, current_user.username)


@farmRouter.patch("/farm/{farm_id}/AC/{ac_id}/automation", response_model=ResponseDto, tags=["Farm"])
async def update_ac_automation(ac_id: int, farm_id: int, is_turn_on: bool, current_user: User = Depends(get_current_active_user)):

    return update_ac_automation_by_id(ac_id, farm_id, is_turn_on, current_user.username)


@farmRouter.patch("/farm/{farm_id}/AC/automation", response_model=ResponseDto, tags=["Farm"])
async def update_all_ac_automations(farm_id: int, is_turn_on: bool, current_user: User = Depends(get_current_active_user)):

    return update_automation_to_all_acs(farm_id, is_turn_on, current_user.username)


@farmRouter.patch("/farm/{farm_id}/{preset_id}/update_all_light_combination}",
                  response_model=ResponseDto[UpdateLightStrengthInputInPreset], tags=["Farm"])
async def apply_light_strength_to_all_in_preset(updateLightStrengthInputInPreset: UpdateLightStrengthInputInPreset,
                                        preset_id: int,
                                        farm_id: int,
                                        current_user: User = Depends(get_current_active_user)):

    return apply_light_strength_to_all_lights_in_preset(updateLightStrengthInputInPreset, farm_id, preset_id, current_user.username)


@farmRouter.patch("/farm/{farm_id}/light/{light_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_light_strength_in_farm(update_input: UpdateLightStrengthInput,
                                        farm_id: int,
                                        light_id: int,
                                        current_user: User = Depends(get_current_active_user)):

    return update_light_strength(update_input, farm_id, light_id, current_user.username)


@farmRouter.patch("/farm/{farm_id}/{preset_id}/{light_combination_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_light_strength_in_preset(update_input: UpdateLightStrengthInput,
                                        farm_id: int,
                                        preset_id: int,
                                        light_combination_id: int,
                                        current_user: User = Depends(get_current_active_user)):

    return update_light_combination_strength(update_input, farm_id, preset_id, light_combination_id, current_user.username)


@farmRouter.put("/farm/{farm_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_farm_name(name: str, farm_id: int, current_user: User = Depends(get_current_active_user)):

    return update_farm_name_to_db(name, farm_id, current_user.username)


@farmRouter.put("/farm/{farm_id}/{preset_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_preset_name(name: str, farm_id: int, preset_id: int, current_user: User = Depends(get_current_active_user)):

    return update_preset_name_to_db(name, farm_id, preset_id, current_user.username)


@farmRouter.put("/farm/{farm_id}/light/{light_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_light_name(name: str, farm_id: int, light_id: int, current_user: User = Depends(get_current_active_user)):

    return update_light_name_to_db(name, farm_id, light_id, current_user.username)


@farmRouter.put("/farm/{farm_id}/AC/{ac_id}}", response_model=ResponseDto, tags=["Farm"])
async def update_ac_name(name: str, farm_id: int, ac_id: int, current_user: User = Depends(get_current_active_user)):

    return update_AC_name_to_db(name, farm_id, ac_id, current_user.username)

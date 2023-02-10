from fastapi import APIRouter, Depends

# OAuth Libraries
from auth.utils import get_current_active_user
from response.response_dto import ResponseDto

from auth.models import User
from .utils import link_farm_to_user, list_farms, list_light, get_light_in_preset, list_light_preset, list_acs, get_light_strength

from .models import FarmOwner, FarmStats, Light, LightCombination, FarmLightPreset, LightStrength

farmRouter = APIRouter()


@farmRouter.post("/add", response_model=ResponseDto[FarmOwner], tags=["Farm"])
async def add_farm_to_user(farm_key: str, current_user: User = Depends(get_current_active_user)):

    return link_farm_to_user(current_user.username, farm_key)


@farmRouter.get("/list", response_model=ResponseDto[FarmStats], tags=["Farm"])
async def list_all_farms(current_user: User = Depends(get_current_active_user)):

    return list_farms(current_user.username)


@farmRouter.get("/farm/{farm_id}/light/list", response_model=ResponseDto[Light], tags=["Farm"])
async def list_all_lights(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_light(farm_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/light/preset/{preset_id}", response_model=ResponseDto[LightCombination], tags=["Farm"])
async def show_light_from_preset(farm_id: int, preset_id: int, current_user: User = Depends(get_current_active_user)):

    return get_light_in_preset(farm_id, preset_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/light/preset", response_model=ResponseDto[FarmLightPreset], tags=["Farm"])
async def list_all_light_preset(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_light_preset(farm_id, current_user.username)


@farmRouter.get("/farm/{farm_id}/AC/list/", response_model=ResponseDto[LightCombination], tags=["Farm"])
async def list_all_acs(farm_id: int, current_user: User = Depends(get_current_active_user)):

    return list_acs(farm_id, current_user.username)
    
    
@farmRouter.get("/farm/{farm_id}/light/{light_id}}", response_model=ResponseDto[LightStrength], tags=["Farm"])
async def get_list_light_strength(light_id: int, farm_id: int, current_user: User = Depends(get_current_active_user)):

    return get_light_strength(light_id, farm_id, current_user.username)



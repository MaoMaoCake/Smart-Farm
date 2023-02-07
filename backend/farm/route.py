from fastapi import APIRouter, Depends

# OAuth Libraries
from auth.utils import get_current_active_user
from response.response_dto import ResponseDto

from auth.models import User
from .utils import link_farm_to_user, list_farms

from .models import FarmOwner

farmRouter = APIRouter()

@farmRouter.post("/add", response_model=ResponseDto[FarmOwner], tags=["Farm"])
async def add_farm_to_user(farm_key: str, current_user: User = Depends(get_current_active_user)):

    return link_farm_to_user(current_user.username, farm_key)

@farmRouter.get("/list", response_model=ResponseDto[FarmOwner], tags=["Farm"])
async def list_all_farms(current_user: User = Depends(get_current_active_user)):

    return list_farms(current_user.username)
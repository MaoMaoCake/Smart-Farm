# env vars
import os

from fastapi import APIRouter, Depends, HTTPException, status

# OAuth Libraries
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .utils import create_access_token, get_current_active_user, create_new_user

from .models import Token, User
from .utils import authenticate_user, create_new_user

from database.enum_list import Role

authRouter = APIRouter()


@authRouter.post("/token", response_model=Token, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Takes Username and password from form data and signs a token
    :param form_data:
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@authRouter.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Temporary endpoint to show how to use login
    :param current_user:
    :return:
    """
    return current_user

@authRouter.post("/users/create", response_model=User)
async def create_user(
        username: str,
        password: str,
        email: str,
        role: Role,
        current_user: User = Depends(get_current_active_user)):

    return create_new_user(username, password, email, role, current_user.username)
# env vars
import os

from fastapi import APIRouter, Depends, HTTPException, status

# OAuth Libraries
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .utils import create_access_token, get_current_active_user

from .models import Token, User
from .utils import authenticate_user

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

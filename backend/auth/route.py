# env vars
import os

from fastapi import APIRouter, Depends, HTTPException, status

# OAuth Libraries
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .utils import create_access_token, get_current_active_user, validate_verification_url, verify_user, forget_password

from .models import Token, User, RegisterInput, ForgetPasswordInput, PasswordChangingInput
from .utils import authenticate_user, create_new_user, is_password_change, reset_password, create_admin, update_admin

from database.enum_list import Role
from response.response_dto import get_response_status, ResponseDto
from response.error_codes import get_http_exception

authRouter = APIRouter(prefix="/api")


@authRouter.post("/token", response_model=ResponseDto, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Takes Username and password from form data and signs a token
    :param form_data:
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        get_http_exception('10','Incorrect username or password')

    access_token_expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return get_response_status(data=Token(access_token=access_token, token_type="bearer", role=user.role))

@authRouter.post("/token_swagger", response_model=Token, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Takes Username and password from form data and signs a token
    :param form_data:
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        get_http_exception('10','Incorrect username or password')

    access_token_expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@authRouter.get("/users/me/", response_model=ResponseDto)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Temporary endpoint to show how to use login
    :param current_user:
    :return:
    """
    return get_response_status(data=current_user)

@authRouter.post("/users/create", response_model=ResponseDto)
async def create_user(form_data: RegisterInput = Depends()):
    return get_response_status(data=create_new_user(form_data.username, form_data.password, form_data.email, form_data.role))


@authRouter.post("/users/verify/{verification_code}", response_model=ResponseDto)
async def verify_email(verification_code: str):
    if validate_verification_url(verification_code):
        return verify_user(verification_code)

    return get_http_exception('10','Verification url timeout')


@authRouter.post("/users/forget-password/", response_model=ResponseDto)
async def forget_email_request(inputs: ForgetPasswordInput = Depends()):
    forget_password(inputs.email)

    return get_response_status('Success')


@authRouter.get("/users/password-changing/{code}", response_model=ResponseDto)
async def get_is_password_changing(code: str):
    return get_response_status(data=is_password_change(code))


@authRouter.patch("/users/change-password/", response_model=ResponseDto)
async def change_password(inputs: PasswordChangingInput = Depends()):
    reset_password(inputs.code, inputs.new_password)
    return get_response_status('Success')


@authRouter.post("/admin/create/admin", response_model=ResponseDto, tags=["Admin"])
async def create_admin_user(inputs: ForgetPasswordInput = Depends()):

    return get_response_status(data=create_admin(inputs.email))


@authRouter.post("/admin/update/admin", response_model=ResponseDto, tags=["Admin"])
async def update_admin_user(form_data: RegisterInput = Depends()):

    return get_response_status(data=update_admin(form_data.username, form_data.password, form_data.email))

# import security modules
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# user model
from .models import User, TokenData

# creating jwt
from datetime import timedelta, datetime
from jose import JWTError, jwt

# fast API tools
from fastapi import Depends, HTTPException, status

# import env variable tools
import os

from database.connector import get_user_from_db, create_user, get_dup_email

from response.error_codes import get_http_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Takes in the plain password and verifies that its is the same as the password stored in the system
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get the hash of the password
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> User | None:
    """
    Takes in a username and password and returns a User Class
    :param username:
    :param password:
    :return:
    """
    user = get_user_from_db(username)

    if not user:
        get_http_exception('10', 'username not found')

    if verify_password(password, user.password):
        return User(username=user.username, role=user.role)
    else:
        return None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generates a JWT for the user
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("OAUTH_SECRET_KEY"), algorithm=os.getenv("OAUTH_ALGORITHM"))
    return encoded_jwt


def get_user(username: str) -> User | None:
    """
    Gets username and returns the User Class
    :param username:
    :return: User class
    """
    user = get_user_from_db(username)

    if not user:
        get_http_exception('10', 'username not found')

    return User(username=user.username, role=user.role)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("OAUTH_SECRET_KEY"), algorithms=[os.getenv("OAUTH_ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def create_new_user(
        username: str,
        password: str,
        email: str,
        role: str,
        create_by: str
    ) -> User:
    if get_user_from_db(username):
        get_http_exception('US401')

    if get_dup_email(email):
        get_http_exception('US402')

    return create_user(username, get_password_hash(password), email, str(role.value), create_by)
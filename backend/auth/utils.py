# import security modules
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer
import base64

# user model
from .models import User, TokenData

# creating jwt
from datetime import timedelta, datetime
from jose import JWTError, jwt

# fast API tools
from fastapi import Depends, HTTPException, status

# import env variable tools
import os

from database.connector import get_user_from_db, create_user, get_dup_email, verify_user_from_verification_code

from response.error_codes import get_http_exception
from response.response_dto import get_response_status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token_swagger")

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

    if not user.verified:
        get_http_exception('10', 'this account has not been verified, Please check the email')
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
    try:
        payload = jwt.decode(token, os.getenv("OAUTH_SECRET_KEY"), algorithms=[os.getenv("OAUTH_ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            get_http_exception('10', "Could not validate credentials")
        token_data = TokenData(username=username)
    except JWTError:
        get_http_exception('10', "Could not validate credentials")
    user = get_user(username=token_data.username)
    if user is None:
        get_http_exception('10', "Could not validate credentials")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def generate_verification_url(email):
    serializer = URLSafeTimedSerializer(os.environ['EMAIL_PASSWORD'])
    verification_code = serializer.dumps(email)
    return f"http://{os.environ['APP_BASE_URL']}/verify/{verification_code}", verification_code


def validate_verification_url(token):
    serializer = URLSafeTimedSerializer(os.environ['EMAIL_PASSWORD'])
    try:
        user_email = serializer.loads(token, max_age=86400)
    except:
        return None
    return user_email


def create_new_user(
        username: str,
        password: str,
        email: str,
        role: str,
    ) -> User:
    if get_user_from_db(username):
        get_http_exception('US401')

    if get_dup_email(email):
        get_http_exception('US402')

    verification_url, verification_code = generate_verification_url(email)
    user = create_user(username, get_password_hash(password), email, str(role.value), 'ADMIN', verification_code)
    send_verification_email(email, verification_url)

    return user


def send_verification_email(to_email, verification_url):
    # Gmail account credentials
    email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    # Email content
    message = MIMEMultipart('alternative')
    message['From'] = email
    message['To'] = to_email
    message['Subject'] = 'Verify your email address'

    html = f"""\
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    .container {{
                        width: 600px;
                        margin: 0 auto;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 20px;
                    }}
                    .logo {{
                        display: block;
                        margin: 0 auto;
                        width: 200px;
                        height: auto;
                    }}
                    .button {{
                        display: block;
                        margin: 0 auto;
                        padding: 10px 20px;
                        background-color: #007bff;
                        color: #fff;
                        text-decoration: none;
                        border-radius: 5px;
                        text-align: center;
                    }}
                    .content {{
                        height: 500px;
                        overflow: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <img class="logo" src="https://cdn.discordapp.com/attachments/802176047096922175/1091638749827444736/logo.png">
                    <h1>Verify your email address</h1>
                    <p>Thanks for signing up! To complete your registration, please click the button below to verify your email address:</p>
                    <p><a class="button" href="{verification_url}">Verify</a></p>
                </div>
            </body>
        </html>
        """
    body = MIMEText(html, 'html')
    message.attach(body)

    # Email server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    context = ssl.create_default_context()

    # Start TLS connection with Gmail server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()

    # Login to Gmail account
    server.login(email, password)

    # Send email and close connection
    server.sendmail(email, to_email, message.as_string())
    server.quit()


def verify_user(verification_code: str):
    if verify_user_from_verification_code(verification_code):
        return get_response_status('Verification success')
    else:
        get_http_exception('10', 'Invalid verification key')
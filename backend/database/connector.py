import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.models import User
from .schemas import UserDb

engine = create_engine(f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                       f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}")

Session = sessionmaker(bind=engine)
session = Session()

def create_user(username: str, password_hashed: str, email: str, role: str) -> None:
    new_user = UserDb(username=username,
                    password=password_hashed,
                    email=email,
                    role=role,
                    createBy=username,
                    updateBy=username
                    )
    session.add(new_user)
    session.commit()


def get_user_from_db(username: str) -> User | None:
    user = session.query(UserDb.username, UserDb.role, UserDb.password).filter(UserDb.username==username).first()

    return User(username=user.username, password=user.password, role=str(user.role.value)) if user else None

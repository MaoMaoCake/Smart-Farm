import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from auth.models import User
from farm.models import FarmOwner
from .schemas import UserDb, FarmOwnerDB, FarmDb

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
    user = session.query(UserDb.id, UserDb.username, UserDb.role, UserDb.password).filter(UserDb.username==username).first()

    return User(id=user.id, username=user.username, password=user.password, role=str(user.role.value)) if user else None

def add_farm_to_user_db(user: User, farm_id:str) -> FarmOwner | None:
    try:
        farm_owner = FarmOwnerDB(farmId=farm_id, userId=user.id, createBy= user.username, updateBy= user.username)
        session.add(farm_owner)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception("Database error occurred") from e

    return FarmOwner(id=farm_owner.id, farmId=farm_owner.farmId, userId=farm_owner.userId)

def check_farm_key_exist(farm_key: str) -> int | None:
    farm = session.query(FarmDb.id).filter(FarmDb.farmKey == farm_key).first()

    return farm.id if farm else None

def check_farm_owning(user_id: int, farm_id: int) -> int | None:
    farm_owning = session.query(FarmOwnerDB.id).filter(FarmOwnerDB.farmId == farm_id
                                                and FarmOwnerDB.userId == user_id ).first()

    return farm_owning.id if farm_owning else None

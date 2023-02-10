import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from auth.models import User
from farm.models import FarmOwner, FarmStats, Light, LightCombination, FarmLightPreset, AC
from .schemas import UserDb, FarmOwnerDB, FarmDb, TemperatureSensorDB, ACDB, HumiditySensorDB, DehumidifierDB, CO2SensorDB, CO2ControllerDB, LightDB, FarmLightPresetDB, LightCombinationDB
from response.error_codes import get_http_exception

engine = create_engine(f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                       f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}")

Session = sessionmaker(bind=engine)
session = Session()


def create_user(username: str, password_hashed: str, email: str, role: str, create_by: str) -> User:
    new_user = UserDb(username=username,
                    password=password_hashed,
                    email=email,
                    role=role,
                    createBy=create_by,
                    updateBy=create_by
                    )
    session.add(new_user)
    session.commit()

    return User(id=new_user.id, username=new_user.username, email=new_user.email, role=str(new_user.role.value))


def get_user_from_db(username: str) -> User | None:
    user = session.query(UserDb.id, UserDb.username, UserDb.role, UserDb.password).filter(UserDb.username==username).first()

    return User(id=user.id, username=user.username, password=user.password, role=str(user.role.value)) if user else None


def get_dup_email(email: str) -> User | None:
    user = session.query(UserDb.id, UserDb.username, UserDb.role, UserDb.password).filter(UserDb.email==email).first()

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
                                                 ,FarmOwnerDB.userId == user_id).first()

    return farm_owning.id if farm_owning else None


def list_farms_from_user_id(user_id: int) -> [FarmStats]:
    farm_owning = session.query(FarmOwnerDB.farmId).filter(FarmOwnerDB.userId == user_id).all()
    farm_ids = [farm[0] for farm in farm_owning]

    farms = session.query(FarmDb.id,
                          FarmDb.name,
                          TemperatureSensorDB.temperature,
                          ACDB.status,
                          HumiditySensorDB.humidity,
                          DehumidifierDB.status,
                          FarmDb.lightStatus,
                          CO2SensorDB.CO2,
                          CO2ControllerDB.status,
                    ).join(TemperatureSensorDB, FarmDb.id == TemperatureSensorDB.farmId
                    ).join(ACDB, FarmDb.id == ACDB.farmId
                    ).join(HumiditySensorDB, FarmDb.id == HumiditySensorDB.farmId
                    ).join(DehumidifierDB, FarmDb.id == DehumidifierDB.farmId
                    ).join(CO2SensorDB, FarmDb.id == CO2SensorDB.farmId
                    ).join(CO2ControllerDB, FarmDb.id == CO2ControllerDB.farmId
                    ).filter(FarmDb.id.in_(farm_ids)).all()

    return [FarmStats(*farm) for farm in farms]


def check_farm_exist(farm_id: int) -> None:
    farm = session.query(FarmDb.id).filter(FarmDb.id == farm_id).first()
    if not farm:
        get_http_exception('FM404')
    return None


def get_lights_from_db(farm_id: int) -> [Light]:
    farm_lights = session.query(LightDB).filter(LightDB.farmId == farm_id).all()

    return [Light(lightId=light.id,
                    lightName=light.name,
                    isAutomation=light.automation,
                    UVLightDensity=light.UVLightDensity,
                    IRLightDensity=light.IRLightDensity,
                    naturalLightDensity=light.naturalLightDensity)
              for light in farm_lights]


def get_lights_from_preset_db(preset_id: int) -> [LightCombination]:
    farm_lights = session.query(LightDB.name,
                               LightCombinationDB.id,
                               LightCombinationDB.lightId,
                               LightCombinationDB.UVLightDensity,
                               LightCombinationDB.IRLightDensity,
                               LightCombinationDB.naturalLightDensity).\
                                join(LightCombinationDB, LightCombinationDB.lightId == LightDB.id)\
                                .filter(LightCombinationDB.farmLightPresetId == preset_id).all()

    return [LightCombination(*light) for light in farm_lights]


def check_preset_exist(preset_id: int) -> None:
    preset = session.query(FarmLightPresetDB.id).filter(FarmLightPresetDB.id == preset_id).first()
    if not preset:
        get_http_exception('PS404')
    return None


def check_preset_owning(farm_id: int, preset_id: int) -> int | None:
    preset_owning = session.query(FarmLightPresetDB.id, FarmLightPresetDB.farmId).filter(FarmLightPresetDB.farmId == farm_id
                                                       , FarmLightPresetDB.id == preset_id).first()

    return FarmLightPresetDB.id if preset_owning else None


def get_light_presets_from_db(farm_id: int) -> [FarmLightPreset]:
    farm_light_presets = session.query(FarmLightPresetDB).filter(FarmLightPresetDB.farmId == farm_id).all()

    return [FarmLightPreset(
        name=preset.name,
        preset_id=preset.farmId
    ) for preset in farm_light_presets]


def get_acs_from_db(farm_id: int) -> [AC]:
    acs = session.query(ACDB).filter(ACDB.farmId == farm_id).all()

    return [AC(
        ACId=ac.id,
        ACName=ac.name,
        ACStatus=ac.status
    ) for ac in acs]

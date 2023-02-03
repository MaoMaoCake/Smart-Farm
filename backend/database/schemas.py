from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base

from .utils import current_datetime
from .enum_list import Role

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    customData = Column(JSON, nullable=True)
    createAt = Column(DateTime, nullable=False, default=current_datetime())
    updateAt = Column(DateTime, nullable=False, default=current_datetime(), onupdate=current_datetime())
    deleteAt = Column(DateTime, nullable=True)
    createBy = Column(String, nullable=False)
    updateBy = Column(String, nullable=False)
    deleteBy = Column(String, nullable=True)

class UserDb(BaseModel):
    __tablename__ = "user"
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)

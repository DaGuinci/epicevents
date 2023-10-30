from models.base import Base

from enum import IntEnum

from sqlalchemy.orm import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum
    )

# Base = declarative_base()


class department(IntEnum):
    COM = 1  # Commercial
    MAN = 2  # Management
    SUP = 3  # Support


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(120), nullable=False)
    role = Column(Enum(department), nullable=False)

    def __repr__(self):
        return f'User {self.name}'

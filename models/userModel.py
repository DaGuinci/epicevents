from models.base import Base

from enum import IntEnum

from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Text,
    UniqueConstraint
    )


# class department(IntEnum):
#     COM = 1  # Commercial
#     MAN = 2  # Management
#     SUP = 3  # Support


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    role = Column(String(3), nullable=False)

    clients = relationship("Client", cascade="all, delete")

    __table_args__ = (UniqueConstraint(
        "name",
        "email",
        name="user_allready_exists"
        ),)

    # def __init__(self):
    #     match self.role:
    #         case 'MAN':
    #             self.permissions =

    def __repr__(self):
        return f'User {self.name}'

from models.base import Base

# from models.userModel import User

import datetime

from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    UniqueConstraint
    )


class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    epic_contact = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    company = Column(String(50), nullable=False)
    date_created = Column(Date, default=datetime.datetime.now)
    date_updated = Column(Date, onupdate=datetime.datetime.now)

    contracts = relationship("Contract", cascade="all, delete")

    __table_args__ = (UniqueConstraint(
        "name",
        "email",
        name="client_allready_exists"
        ),)

    def __repr__(self):
        return f'Client {self.name}'

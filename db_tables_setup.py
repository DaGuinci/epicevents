from enum import IntEnum
import datetime
import json

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.engine import URL

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    Date,
    Enum,
    Boolean,
    Text,
    UniqueConstraint
    )

Base = declarative_base()


class department(IntEnum):
    COM = 1  # Commercial
    MAN = 2  # Management
    SUP = 3  # Support


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    role = Column(Enum(department), nullable=False)

    clients = relationship("Client", cascade="all, delete")

    __table_args__ = (UniqueConstraint(
        "name",
        "email",
        name="user_allready_exists"
        ),)

    def __repr__(self):
        return f'User {self.name}'


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


class Contract(Base):
    __tablename__ = 'contract'

    contract_id = Column(Integer, primary_key=True)
    client = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    total_amount = Column(Float(2), nullable=False)
    due_amount = Column(Float(2))
    signed = Column(Boolean, default=False)
    date_created = Column(Date, default=datetime.datetime.now)

    events = relationship("Event", cascade="all, delete")

    def __repr__(self):
        return f'Contract {self.contract_id}'


class Event(Base):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    contract = Column(
        Integer, ForeignKey("contract.contract_id"), nullable=False
        )
    name = Column(String(50), nullable=False)
    epic_contact = Column(Integer, ForeignKey("user.user_id"))
    date_start = Column(Date)
    date_end = Column(Date)
    location = Column(String(50))
    attendees = Column(Integer)
    notes = Column(Text)

    def __repr__(self):
        return f'Event {self.name}'


f = open('config.json')
config = json.load(f)
f.close()

credentials = config['test_db_config']

url = URL.create(
    drivername="postgresql",
    username=credentials['db_user'],
    password=credentials['db_pass'],
    host="localhost",
    database=credentials['db_name']
)
engine = create_engine(url, echo=False)

Base.metadata.create_all(engine)

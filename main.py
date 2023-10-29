import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text,
    Date,
    Boolean,
    ForeignKey,
    Enum
    )
from sqlalchemy.orm import Session

from enum import IntEnum

Base = declarative_base()


url = URL.create(
    drivername="postgresql",
    username="epic_user",
    password="epicpass",
    host="localhost",
    database="epiceventsdb"
)


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

# Base.metadata.create_all(engine)


engine = create_engine(url, echo=True)

with Session(engine) as session:
    first_user = User(
        name='first_user',
        email='first@user.com',
        password='firstpass',
        role='MAN'
    )
    session.add(first_user)

    session.commit()

    first_client = Client(
        epic_contact=first_user.user_id,
        name='First client',
        email='first@client.com',
        phone='633922975',
        company='Wayne Corp'
    )
    session.add(first_client)
    session.commit()

    first_contract = Contract(
        client=first_client.client_id,
        total_amount=341.23,
    )
    session.add(first_contract)
    session.commit()

    first_event = Event(
        contract=first_contract.contract_id,
        name='My first event',
    )
    session.add(first_event)
    session.commit()

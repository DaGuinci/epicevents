from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Date,
    Boolean,
    Text,
    UniqueConstraint
    )

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    contract = Column(
        String, ForeignKey("contract.contract_id"), nullable=False
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


class Contract(Base):
    __tablename__ = 'contract'

    contract_id = Column(String, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    total_amount = Column(Float(2))
    due_amount = Column(Float(2))
    signed = Column(Boolean, default=False)
    date_created = Column(Date, default=datetime.datetime.now)

    # events = relationship("Event", cascade="all, delete")
    client = relationship(
        "Client",
        backref="contracts"
        )
    def __repr__(self):
        return f'Contract {self.contract_id}'


class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    epic_contact_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    company = Column(String(50), nullable=False)
    date_created = Column(Date, default=datetime.datetime.now)
    date_updated = Column(Date, onupdate=datetime.datetime.now)

    # contracts = relationship("Contract", cascade="all, delete")
    epic_contact = relationship(
        "User",
        backref="clients"
        )

    __table_args__ = (UniqueConstraint(
        "name",
        "email",
        name="client_allready_exists"
        ),)

    def __repr__(self):
        return f'Client {self.name}'


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    role = Column(String(3), nullable=False)

    # clients = relationship("Client", cascade="all, delete")

    __table_args__ = (UniqueConstraint(
        "name",
        "email",
        name="user_allready_exists"
        ),)

    def __repr__(self):
        return f'User {self.name}'


def create_tables(engine):
    Base.metadata.create_all(engine)

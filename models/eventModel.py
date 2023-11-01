from models.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Text
    )


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

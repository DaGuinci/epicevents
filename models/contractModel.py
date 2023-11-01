from models.base import Base

import datetime

from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    Date,
    Boolean
    )


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



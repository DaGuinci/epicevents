from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.userModel import User
from models.clientModel import Client
from models.contractModel import Contract
from models.eventModel import Event


class DataController():

    def __init__(self, credentials):

        url = URL.create(
            drivername="postgresql",
            username=credentials['db_user'],
            password=credentials['db_pass'],
            host="localhost",
            database="epiceventsdb"
        )
        self.engine = create_engine(url, echo=True)

    def read_datas(self):
        with Session(self.engine) as session:
            stmt = select(User).where(User.name.in_(["first_user"]))

            for user in session.scalars(stmt):
                print(user)

            # first_user = User(
            #     name='first_user',
            #     email='first@user.com',
            #     password='firstpass',
            #     role='MAN'
            # )
            # session.add(first_user)

            # session.commit()

            # first_client = Client(
            #     epic_contact=first_user.user_id,
            #     name='First client',
            #     email='first@client.com',
            #     phone='633922975',
            #     company='Wayne Corp'
            # )
            # session.add(first_client)
            # session.commit()

            # first_contract = Contract(
            #     client=first_client.client_id,
            #     total_amount=341.23,
            # )
            # session.add(first_contract)
            # session.commit()

            # first_event = Event(
            #     contract=first_contract.contract_id,
            #     name='My first event',
            # )
            # session.add(first_event)
            # session.commit()
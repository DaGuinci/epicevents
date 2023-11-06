from sqlalchemy.engine import URL
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session

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
            database=credentials['db_name']
        )
        self.engine = create_engine(url, echo=False)
        self.session = Session(self.engine)

    # Users
    # def save_user(self, args):
    #     # hash password
    #     new_user = User(
    #         name=args['name'],
    #         email=args['email'],
    #         password=args['password'],
    #         role=args['role']
    #     )
    #     self.session.add(new_user)
    #     return self.session.commit()

    def get_users(self):
        with Session(self.engine) as session:
            stmt = select(User)
            users = []
            for user in session.scalars(stmt):
                users.append(user)
        return users

    def get_user_by_name(self, name):
        with Session(self.engine) as session:
            stmt = select(User).where(User.name == name)
            users = []
            for user in session.scalars(stmt):
                users.append(user)
        return users

    def get_user_by_id(self, id):
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user:
                return user
            else:
                return False

    def delete_user(self, id):
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user:
                session.delete(user)
                session.commit()
                return True
            else:
                return False

    # Clients
    def create_client(self, args):
        with Session(self.engine) as session:
            new_client = Client(
                name=args['name'],
                email=args['email'],
                phone=args['phone'],
                epic_contact=args['epic_contact'],
                company=args['company'],
            )
            session.add(new_client)
            session.commit()
        return True

    def get_clients(self):
        with Session(self.engine) as session:
            stmt = select(Client)
            clients = []
            for client in session.scalars(stmt):
                clients.append(client)
        return clients

    # Contracts
    def create_contract(self, args):
        with Session(self.engine) as session:
            new_contract = Contract(
                client=args['client'],
                total_amount=args['total_amount'],
            )
            session.add(new_contract)
            session.commit()
        return True

    def get_contracts(self):
        with Session(self.engine) as session:
            stmt = select(Contract)
            contracts = []
            for contract in session.scalars(stmt):
                contracts.append(contract)
        return contracts

    # Events
    def create_event(self, args):
        with Session(self.engine) as session:
            new_event = Event(
                contract=args['contract'],
                name=args['name'],
            )
            session.add(new_event)
            session.commit()
        return True

    def get_events(self):
        with Session(self.engine) as session:
            stmt = select(Event)
            events = []
            for event in session.scalars(stmt):
                events.append(event)
        return events

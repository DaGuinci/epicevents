import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest import TestCase
from sqlalchemy.engine import URL
from sqlalchemy import select

from models.userModel import User
from models.clientModel import Client
from models.contractModel import Contract
from models.eventModel import Event


class TempDatabaseTest(TestCase):

    # get the local test database credentials
    f = open('config.json')
    config = json.load(f)
    f.close()
    credentials = config['test_db_config']

    def setUp(self):

        # make url
        url = URL.create(
            drivername="postgresql",
            username=self.credentials['db_user'],
            password=self.credentials['db_pass'],
            host="localhost",
            database=self.credentials['db_name']
        )

        Session = sessionmaker()

        engine = create_engine(url)

        self.connection = engine.connect()

        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def clean_db(self):

        # Delete all events
        events = self.session.query(Event).all()
        for event in events:
            self.session.delete(event)

        # Delete all contracts
        contracts = self.session.query(Contract).all()
        for contract in contracts:
            self.session.delete(contract)

        # Delete all clients
        clients = self.session.query(Client).all()
        for client in clients:
            self.session.delete(client)

        # Delete all users
        users = self.session.query(User).all()
        for user in users:
            self.session.delete(user)
        self.session.commit()

    def tearDown(self):

        self.clean_db()

        self.session.close()
        # return connection to the Engine
        self.connection.close()

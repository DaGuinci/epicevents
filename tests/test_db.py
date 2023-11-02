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

    # get the local database credentials
    f = open('config.json')
    credentials = json.load(f)
    f.close()

    def setUp(self):

        # make url
        url = URL.create(
            drivername="postgresql",
            username=self.credentials['db_user'],
            password=self.credentials['db_pass'],
            host="localhost",
            database="epiceventsdb"
        )

        # global application scope.  create Session class, engine
        Session = sessionmaker()

        engine = create_engine(url)
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection, selecting
        # "create_savepoint" join_transaction_mode
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def select_users(self):
        stmt = select(User)

        for user in self.session.scalars(stmt):
            print('************')
            print(user)
            pass

    def test_something(self):
        # use the session in tests.
        user_test = User(
            name='test_user_3',
            email='test@user.com',
            password='testpass',
            role='MAN'
        )
        self.session.add(user_test)
        self.session.commit()
        users = self.session.query(User).all()
        print('--------------------')
        print(users)
        # pass

    def test_something_with_rollbacks(self):
        user_test = User(
            name='test_user',
            email='test@user.com',
            password='testpass',
            role='MAN'
        )
        self.session.add(user_test)
        self.select_users()
        self.session.flush()
        self.session.rollback()

        # self.session.add(Foo())
        self.session.commit()

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest import TestCase
from sqlalchemy.engine import URL
from sqlalchemy import select

from models.userModel import User

f = open('config.json')
credentials = json.load(f)
f.close()

url = URL.create(
    drivername="postgresql",
    username=credentials['db_user'],
    password=credentials['db_pass'],
    host="localhost",
    database="epiceventsdb"
)
# global application scope.  create Session class, engine
Session = sessionmaker()

engine = create_engine(url)


class SomeTest(TestCase):
    def setUp(self):
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
            # print(user)
            pass

    # def test_something(self):
    #     # use the session in tests.

    #     # self.session.add(Foo())
    #     # self.session.commit()
    #     pass

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
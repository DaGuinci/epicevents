from test_db import TempDatabaseTest

from controllers.dbController import DataController

from models.userModel import User


class UserControllerTest(TempDatabaseTest):
    def test_user_creation(self):
        self.setUp()
        controller = DataController(self.credentials)

        """
        When creating a user
        Then the user is written in the database
        """
        args = {
            'name': 'Benjamin Franklin',
            'email': 'benjamin@franklin.com',
            'password': 'benjpass',
            'role': 'MAN'
        }
        controller.create_user(args)

        response = self.session.query(User).filter(User.name == 'Benjamin Franklin').first()
        print('&&&&&&&&&&&&&&&&&')
        print(response)
        self.session.flush()
        self.session.rollback()
        self.tearDown()
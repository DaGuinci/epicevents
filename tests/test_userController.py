from test_db import TempDatabaseTest

from controllers.dbController import DataController

from models.userModel import User


class UserControllerTest(TempDatabaseTest):

    def test_user_creation(self):
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
        assert controller.create_user(args) is True

        # response = self.session.query(User).filter(User.name == 'Benjamin ranklin').first()
        assert (self.session.query(User).filter(
            User.name == 'Benjamin Franklin'
            ).first()
            is not
            None
            )

        """
        When creating a user with same name and email
        Then an error message is returned
        """
        assert controller.create_user(args) == 'Cet utilisateur existe déjà.'

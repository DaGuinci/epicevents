from controllers.dbController import DataController
from controllers.userController import UserController


class MainController():

    def __init__(self, db_credentials):
        self.data_controller = DataController(db_credentials)
        self.user_controller = UserController(self.data_controller)
        self.logged = None
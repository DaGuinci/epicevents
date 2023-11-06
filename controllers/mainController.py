from controllers.dbController import DataController
from controllers.userController import UserController

from views import formViews, returnViews


class MainController():

    def __init__(self, db_credentials):
        self.data_controller = DataController(db_credentials)
        self.user_controller = UserController(self.data_controller)
        self.return_view = returnViews.ReturnView()
        self.forms_view = formViews.FormView()
        self.logged = None

        self.return_view.welcome()
        self.log_user()

    def log_user(self):
        # recuperer les credentials de l;utilisateur
        credentials = self.forms_view.get_user_log_infos()
        if credentials:
            try_login = self.user_controller.login(credentials)
            if try_login[0] == True:
                #log user
                self.logged = try_login[1]
                print(self.logged)
            else:
                self.return_view.error_msg(try_login)
                self.log_user()

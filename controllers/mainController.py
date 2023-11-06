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
            if try_login['status'] is True:
                #log user
                self.logged = try_login['user']
                if self.logged.role == 'MAN':
                    self.return_view.success_msg({
                        'type': 'user_logged',
                        'user': self.logged
                        })
                    return self.main_manager()
            else:
                self.return_view.error_msg(try_login['error'])
                return self.log_user()

    def main_manager(self):
        # display manager menu
        choice = self.forms_view.manager_main_menu()
        match choice:
            case 0:
                args = self.forms_view.get_user_creation_infos()
                response = self.user_controller.create_user(args)
                if response['status']:
                    self.return_view.success_msg({
                        'type': 'new_user_created',
                        'user': response['user']
                        })
                    self.main_manager()
                else:
                    self.return_view.error_msg(response['error'])
                    self.main_manager()
            case 4:
                exit()
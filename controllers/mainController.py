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
            case 1:
                # TODO proposer une demarche par dept/par recherche...
                self.pick_user()
            case 4:
                exit()

    def pick_user(self):
        users = self.user_controller.get_users()
        options = []
        for user in users:
            options.append(user.name)
        options.append('Revenir en arrière')
        response = self.forms_view.user_choice(options)
        if response == len(options)-1:
            self.main_manager()
        else:
            user = users[response]
            self.user_actions(user)

    def user_actions(self, user):
        self.return_view.user_card(user)
        response = self.forms_view.user_actions_menu()
        match response:
            case 0:
                self.update_user_process(user)
            case 1:
                self.delete_user_process(user)
            case 2:
                self.pick_user()

    def update_user_process(self, user):
        response = self.forms_view.modify_user_menu(user)
        update_return = self.user_controller.update_user(
            user,
            response['key'],
            response['value']
            )
        # if ok, success msg
        if update_return['status']:
            self.return_view.success_msg(
                {
                    'type': 'user_updated',
                    'user': user
                    }
                )
            self.pick_user()
        # if not, error msg
        else:
            self.return_view.error_msg(update_return['error'])
            self.pick_user()
        print(update_return)


    def delete_user_process(self, user):
        pass

from controllers.dbController import DataController
from controllers.userController import UserController
from controllers.clientController import ClientController

from views import formViews, returnViews


class MainController():

    def __init__(self, db_credentials):
        self.data_controller = DataController(db_credentials)
        self.user_controller = UserController(self.data_controller)
        self.client_controller = ClientController(self.data_controller)
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
                self.return_view.success_msg({
                    'type': 'user_logged',
                    'user': self.logged
                    })
                if self.logged.role == 'MAN':
                    return self.main_manager()
                if self.logged.role == 'COM':
                    return self.main_sales()
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
                    return self.main_manager()
                else:
                    self.return_view.error_msg(response['error'])
                    return self.main_manager()
            case 1:
                # TODO proposer une demarche par dept/par recherche...
                return self.pick_user()
            case 4:
                exit()

    def pick_user(self):
        users = self.user_controller.get_users()
        options = []
        for user in users:
            options.append(user.name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'user')
        if response == len(options)-1:
            return self.main_manager()
        else:
            user = users[response]
            return self.user_actions(user)

    def user_actions(self, user):
        self.return_view.user_card(user)
        response = self.forms_view.user_actions_menu()
        match response:
            case 0:
                return self.update_user_process(user)
            case 1:
                return self.delete_user_process(user)
            case 2:
                return self.pick_user()

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
            return self.pick_user()
        # if not, error msg
        else:
            self.return_view.error_msg(update_return['error'])
            return self.pick_user()

    def delete_user_process(self, user):
        username = user.name
        if user == self.logged:
            self.return_view.error_msg(
                'self_deleting'
            )
            return self.pick_user()
        response = self.forms_view.confirm_user_delete(user)
        if response:
            # TODO manage the case of user having clients, contracts...
            delete_return = self.user_controller.delete_user(user)
            if delete_return:
                self.return_view.success_msg(
                    {
                        'type': 'user_deleted',
                        'user': username
                        }
                    )
                self.pick_user()
        else:
            self.pick_user()

    def main_sales(self):
        """Main menu for commercials."""
        choice = self.forms_view.sales_main_menu()
        match choice:
            case 0:
                args = self.forms_view.get_client_creation_infos()
                args['epic_contact'] = self.logged.user_id
                create_return = self.client_controller.create_client(args)
                if create_return['status']:
                    self.return_view.success_msg({
                        'type': 'new_client_created',
                        'client': create_return['client']
                        })
                    return self.main_sales()
                else:
                    self.return_view.error_msg(create_return['error'])
                    return self.main_sales()
            case 1:
                # TODO proposer une demarche par dept/par recherche...
                return self.pick_client()
            case 4:
                exit()

    def pick_client(self):
        clients = self.client_controller.get_user_clients(self.logged)
        # self.main_sales()
        options = []
        for client in clients:
            options.append(client.name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'client')
        if response == len(options)-1:
            return self.main_sales()
        else:
            client = clients[response]
            return self.client_actions(client)

    def client_actions(self, client):
        self.return_view.client_card(client)
        response = self.forms_view.client_actions_menu()
        match response:
            case 0:
                return self.update_client_process(client)
            case 1:
                return self.delete_client_process(client)
            case 2:
                return self.pick_client()

    def update_client_process(self, client):
        """Modify a client"""
        response = self.forms_view.modify_client_menu(client)
        update_return = self.client_controller.update_client(
            client,
            response['key'],
            response['value']
            )
        # if ok, success msg
        if update_return['status']:
            self.return_view.success_msg(
                {
                    'type': 'client_updated',
                    'client': client
                    }
                )
            return self.pick_client()
        # if not, error msg
        else:
            self.return_view.error_msg(update_return['error'])
            return self.pick_client()

    def delete_client_process(self, client):
        clientname = client.name
        response = self.forms_view.confirm_client_delete(client)
        if response:
            # TODO manage the case of client having  contracts...
            delete_return = self.client_controller.delete_client(client)
            if delete_return:
                self.return_view.success_msg(
                    {
                        'type': 'client_deleted',
                        'client': clientname
                        }
                    )
                self.pick_client()
        else:
            self.pick_client()

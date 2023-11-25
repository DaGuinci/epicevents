from controllers.dbController import DataController
from controllers.userController import UserController
from controllers.clientController import ClientController
from controllers.contractController import ContractController
from controllers.eventController import EventController

from views import formViews, returnViews, tools


class MainController():

    def __init__(self, db_credentials):
        self.data_controller = DataController(db_credentials)
        self.user_controller = UserController(self.data_controller)
        self.client_controller = ClientController(self.data_controller)
        self.contract_controller = ContractController(self.data_controller)
        self.event_controller = EventController(self.data_controller)
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
                # TODO proposer une demarche par dept/par recherche...
                return self.pick_user()
            case 1:
                # TODO proposer une demarche par dept/par recherche...
                return self.pick_client()
            case 2:
                return self.pick_contract()
            case 4:
                exit()

    def pick_user(self):
        users = self.user_controller.get_users()
        options = ['Créer un nouveau collaborateur']
        for user in users:
            options.append(user.name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'user')
        if response == 0:
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
        elif response == len(options)-1:
            return self.main_manager()
        else:
            user = users[response-1]
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
        response = self.forms_view.confirm_resource_delete(user, 'user')
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
                # TODO proposer une demarche par dept/par recherche...
                return self.pick_salesman_client()
            case 1:
                return self.pick_salesman_contract()
            case 3:
                return self.create_event_process()
            case 4:
                return self.pick_client()
            case 5:
                exit()

    def pick_client(self):
        clients = self.client_controller.get_clients()
        options = []
        for client in clients:
            options.append(client.name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'client')
        if response == len(options)-1:
            match self.logged.role:
                case 'MAN':
                    return self.main_manager()
                case 'COM':
                    return self.main_sales()
        else:
            client = clients[response]
            return self.read_client(client)

    def read_client(self, client):
        self.return_view.client_card(client)
        tools.prompt_ok()
        return self.pick_client()

    def pick_salesman_client(self):
        clients = self.client_controller.get_salesman_clients(self.logged)
        options = ['Créer un nouveau client']
        for client in clients:
            options.append(client.name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'client')
        if response == 0:
            args = self.forms_view.get_client_creation_infos()
            args['epic_contact'] = self.logged
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
        elif response == len(options)-1:
            return self.main_sales()
        else:
            client = clients[response-1]
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
                match self.logged.role:
                    case 'MAN':
                        return self.pick_client()
                    case 'COM':
                        return self.pick_salesman_client()

    def update_client_process(self, client):
        """Modify a client"""
        response = self.forms_view.modify_client_menu(client)
        if response:
            update_return = self.client_controller.update_client(
                client,
                response['key'],
                response['value']
                )
            if update_return['status']:
                self.return_view.success_msg(
                    {
                        'type': 'client_updated',
                        'client': client
                        }
                    )
                return self.pick_salesman_client()
            # if not, error msg
            else:
                self.return_view.error_msg(update_return['error'])
                return self.pick_salesman_client()
        return self.pick_salesman_client()

    def delete_client_process(self, client):
        clientname = client.name
        response = self.forms_view.confirm_resource_delete(client, 'client')
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

    def pick_contract(self):
        contracts = self.contract_controller.get_contracts()
        options = ['Créer un nouveau contrat']
        for contract in contracts:
            options.append(contract.contract_name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'contracts')
        if response == 0:
            return self.create_contract_process()
        elif response == len(options)-1:
            return self.main_manager()
        else:
            contract = contracts[response-1]
            return self.contract_actions(contract)

    def contract_actions(self, contract):
        self.return_view.contract_card(contract)
        # tools.prompt_ok()
        response = self.forms_view.contract_actions_menu(self.logged.role)
        match response:
            case 0:
                return self.update_contract_process(contract)
            case 1:
                match self.logged.role:
                    case 'MAN':
                        return self.delete_contract_process(contract)
                    case 'COM':
                        return self.pick_salesman_contract()
            case 2:
                return self.pick_contract()
        return self.pick_contract()

    def create_contract_process(self):
        clients = self.client_controller.get_clients()
        options = []
        # TODO case no client
        for client in clients:
            options.append(client.name)
        new_contract_client = self.forms_view.resource_picker(
            options, 'client_for_new_contract'
            )
        response = self.contract_controller.create_contract({
            'client': clients[new_contract_client]
        })
        if response['status']:
            self.return_view.success_msg({
                'type': 'new_contract_created',
                'contract': response['contract']
                })
            return self.main_manager()
        else:
            self.return_view.error_msg(response['error'])
            return self.main_manager()

    def update_contract_process(self, contract):
        response = self.forms_view.modify_contract_menu(contract)
        if response:
            update_return = self.contract_controller.update_contract(
                contract,
                response['key'],
                response['value']
                )
            if update_return['status']:
                self.return_view.success_msg(
                    {
                        'type': 'contract_updated',
                        'contract': contract
                        }
                    )
                match self.logged.role:
                    case 'MAN':
                        return self.pick_contract()
                    case 'COM':
                        return self.pick_salesman_contract()
            # if not, error msg
            else:
                self.return_view.error_msg(update_return['error'])
                match self.logged.role:
                    case 'MAN':
                        return self.pick_contract()
                    case 'COM':
                        return self.pick_salesman_contract()
        return self.pick_contract()

    def delete_contract_process(self, contract):
        contractid = contract.contract_id
        response = self.forms_view.confirm_resource_delete(contract, 'contract')
        if response:
            # TODO manage the case of contract having  contracts...
            delete_return = self.contract_controller.delete_contract(contract)
            if delete_return:
                self.return_view.success_msg(
                    {
                        'type': 'contract_deleted',
                        'contract': contractid
                        }
                    )
                self.pick_contract()
        else:
            self.pick_contract()

    def pick_salesman_contract(self):
        contracts = self.contract_controller.get_salesman_contracts(
            self.logged
            )
        options = []
        for contract in contracts:
            options.append(contract.contract_name)
        options.append('Revenir en arrière')
        response = self.forms_view.resource_picker(options, 'contracts')
        if response == len(options)-1:
            return self.main_sales()
        else:
            contract = contracts[response-1]
            return self.contract_actions(contract)

    def create_event_process(self):
        # ask for target client
        contracts = self.contract_controller.get_salesman_signed_contracts(
            self.logged
            )
        options = []
        if len(contracts) > 0:
            for contract in contracts:
                options.append(
                    contract[0].contract_name +
                    ' pour le client ' +
                    contract[1]
                    )
            options.append('Revenir en arrière')
            response = self.forms_view.resource_picker(
                options,
                'contract_for_event'
                )
            if response == len(options)-1:
                return self.main_sales()
            support_users = self.user_controller.get_sopport_users()
            # TODO case no support users
            args = self.forms_view.get_event_creation_infos(support_users)
            args['contract'] = contracts[response][0]

            create_return = self.event_controller.create_event(args)
            if create_return['status']:
                self.return_view.success_msg({
                    'type': 'new_event_created',
                    'event': create_return['event']
                    })
                return self.main_sales()
        else:
            self.return_view,error_msg('no_signed_contracts')

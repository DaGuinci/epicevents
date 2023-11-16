from simple_term_menu import TerminalMenu
from getpass import getpass

from views import tools


class FormView:

    def get_user_log_infos(self):
        credentials = {}
        credentials['username'] = input('Entrez votre nom d\'utilisateur:\n')
        # print('\n')
        credentials['password'] = getpass('\nEntrez votre mot de passe:\n')
        return credentials

    def manager_main_menu(self):
        tools.clear_term()
        title = 'Gestion: menu principal'
        content = tools.format_title(title)
        options = [
            'Inscrire un collaborateur',
            'Voir ou modifier les collaborateurs',
            'Voir les clients',
            'Voir ou modifier les contrats',
            'Quitter l\'application'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_screen=True,
            title=content,
            quit_keys=()
            )

        return terminal_menu.show()

    def get_user_creation_infos(self):
        print(tools.format_title('Création d\'un collaborateur'))
        infos = {}

        infos['name'] = input('Nom:\n')
        while len(infos['name']) == 0:
            print('Ce champ est obligatoire.\n')
            infos['name'] = input('Nom:\n')

        infos['email'] = input('\nEmail:\n')
        while len(infos['email']) == 0:
            print('Ce champ est obligatoire.')
            infos['email'] = input('\nEmail:\n')

        infos['password'] = input('\nMot de passe:\n')
        while len(infos['password']) == 0:
            print('Ce champ est obligatoire.')
            infos['password'] = input('\nMot de passe:\n')
        print('\nDépartement:')
        options = [
            'Département gestion',
            'Département commercial',
            'Département support',
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            )
        infos['role'] = None
        while infos['role'] not in ['MAN', 'COM', 'SUP']:
            match terminal_menu.show():
                case 0:
                    infos['role'] = 'MAN'
                case 1:
                    infos['role'] = 'COM'
                case 2:
                    infos['role'] = 'SUP'
                case _:
                    print('Ce champ est obligatoire.')
                    print('\nDépartement:')
        return infos

    def resource_picker(self, resources, type):
        """resources = list of str: resource's name
        type = str class name"""
        tools.clear_term()
        match type:
            case 'user':
                title = 'Choisir un collaborateur'
            case 'client':
                title = 'Choisir un client'
            case _:
                title = 'Choisir une ressource'
        terminal_menu = TerminalMenu(
            resources,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title=tools.format_title(title),
            show_shortcut_hints=True
            )
        return terminal_menu.show()

    def user_actions_menu(self):
        options = [
            'Modifier le collaborateur',
            'Supprimer le collaborateur',
            'Revenir en arrière'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title='\nQue souhaitez-vous faire ?'
            )
        return terminal_menu.show()

    def modify_user_menu(self, user):
        tools.clear_term()
        title = 'Modification d\'un collaborateur - ' + user.name
        print(tools.format_title(title))
        options = [
            'Modifier le nom',
            'Modifier le mot de passe',
            'Modifier le courrier électronique',
            'Modifier le département',
            'Revenir en arrière'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title='Que souhaitez-vous modifier ?'
            )
        match terminal_menu.show():
            case 0:
                key = 'name'
                new_value = input('Nouveau nom:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau nom:\n')
            case 1:
                key = 'password'
                new_value = input('Nouveau mot de passe:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau mot de passe:\n')
            case 2:
                key = 'email'
                new_value = input('Nouveau courrier électronique:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau courrier électronique:\n')
            case 3:
                key = 'role'
                departments = [
                    'Département gestion',
                    'Département commercial',
                    'Département support',
                ]
                dept_menu = TerminalMenu(
                    departments,
                    menu_highlight_style=('standout', 'bg_purple'),
                    clear_menu_on_exit=False,
                    quit_keys=(),
                    title='Sélectionner le nouveau département:'
                    )
                new_value = ''
                tools.clear_term()
                choice = dept_menu.show()
                while new_value not in ['MAN', 'COM', 'SUP']:
                    match choice:
                        case 0:
                            new_value = 'MAN'
                        case 1:
                            new_value = 'COM'
                        case 2:
                            new_value = 'SUP'
                        case _:
                            print('Ce champ est obligatoire.')
                            print('\nDépartement:')
        return {
            'key': key,
            'value': new_value
        }

    def confirm_user_delete(self, user):
        tools.clear_term()
        title = tools.format_title('Confirmation de suppression')
        print(title)
        title = (
            'Souhaitez-vous réellement supprimer le collaborateur ' +
            user.name +
            ' ?\n'
            )
        options = [
            'Confirmer',
            'Revenir en arrière',
        ]
        term_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title=title
            )
        match term_menu.show():
            case 0:
                return True
            case 1:
                return False

    def sales_main_menu(self):
        tools.clear_term()
        title = 'Commercial: menu principal'
        content = tools.format_title(title)
        options = [
            'Créer un nouveau client',
            'Voir ou modifier vos clients',
            'Voir ou modifier vos contrats',
            'Voir les contrats non signés',
            'Créer un nouvel événement',
            'Voir tous les clients',
            'Quitter l\'application'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_screen=True,
            title=content,
            quit_keys=()
            )

        return terminal_menu.show()

    def get_client_creation_infos(self):
        print(tools.format_title('Création d\'un collaborateur'))
        infos = {}

        infos['name'] = input('Nom:\n')
        while len(infos['name']) == 0:
            print('Ce champ est obligatoire.\n')
            infos['name'] = input('Nom:\n')

        infos['email'] = input('\nEmail:\n')
        while len(infos['email']) == 0:
            print('Ce champ est obligatoire.')
            infos['email'] = input('\nEmail:\n')

        infos['phone'] = input('\nNuméro de téléphone:\n')
        while len(infos['phone']) == 0:
            print('Ce champ est obligatoire.')
            infos['phone'] = input('\nNuméro de téléphone:\n')

        infos['company'] = input('\nEntreprise:\n')
        while len(infos['company']) == 0:
            print('Ce champ est obligatoire.')
            infos['company'] = input('\nSociété:\n')

        return infos

    def client_actions_menu(self):
        options = [
            'Modifier le client',
            'Supprimer le client',
            'Revenir en arrière'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title='\nQue souhaitez-vous faire ?'
            )
        return terminal_menu.show()

    def modify_client_menu(self, client):
        tools.clear_term()
        title = 'Modification d\'un client - ' + client.name
        print(tools.format_title(title))
        options = [
            'Modifier le nom',
            'Modifier le courrier électronique',
            'Modifier le numéro de téléphone',
            'Modifier l\'entreprise',
            'Revenir en arrière'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title='Que souhaitez-vous modifier ?'
            )
        match terminal_menu.show():
            case 0:
                key = 'name'
                new_value = input('Modifier le nom:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau nom:\n')
            case 1:
                key = 'email'
                new_value = input('Modifier le courrier électronique:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau mot de passe:\n')
            case 2:
                key = 'phone'
                new_value = input('Modifier le numéro de téléphone:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Nouveau courrier électronique:\n')
            case 3:
                key = 'company'
                new_value = input('Modifier l\'entreprise:\n')
                while len(new_value) == 0:
                    print('Ce champ est obligatoire.\n')
                    new_value = input('Modifier l\'entreprise:\n')
            case 4:
                return False
        return {
            'key': key,
            'value': new_value
        }

    def confirm_client_delete(self, client):
        tools.clear_term()
        title = tools.format_title('Confirmation de suppression')
        print(title)
        title = (
            'Souhaitez-vous réellement supprimer le client ' +
            client.name +
            ' ?\n'
            )
        options = [
            'Confirmer',
            'Revenir en arrière',
        ]
        term_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_menu_on_exit=False,
            quit_keys=(),
            title=title
            )
        match term_menu.show():
            case 0:
                return True
            case 1:
                return False
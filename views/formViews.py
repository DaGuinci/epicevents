from simple_term_menu import TerminalMenu

from views import tools


class FormView:

    def get_user_log_infos(self):
        credentials = {}
        credentials['username'] = input('Entrez votre nom d\'utilisateur:\n')
        # print('\n')
        credentials['password'] = input('\nEntrez votre mot de passe:\n')
        return credentials

    def manager_main_menu(self):
        tools.clear_term()
        title = 'Gestion: menu principal'
        content = tools.format_title(title)
        options = [
            'Inscrire un collaborateur',
            'Voir ou modifier les collaborateurs',
            'Voir les clients',
            'Voir les contrats',
            'Quitter l\'application'
        ]
        terminal_menu = TerminalMenu(
            options,
            menu_highlight_style=('standout', 'bg_purple'),
            clear_screen=True,
            title=content
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

from views import tools


class ReturnView:

    def welcome(self):
        tools.clear_term()
        msg = 'EpicEvents / Gestion de clientèle'
        content = msg.center(70, '*')
        print('\n')
        print(content)
        print('\n')

    def welcome_logged(self, user):
        msg = 'Bonjour, ' + user.name
        content = msg.center(35, '*')
        print('\n')
        print(content)
        print('\n')
        tools.prompt_ok()

    def error_msg(self, error_type):
        match error_type:
            case 'bad_username':
                print('\nCet utilisateur n\'existe pas.\n')
            case 'bad_credentials':
                print('\nLe mot de passe et le nom d\'utilisateur ' +
                      'ne correspondent pas.\n')
            case 'existing_user':
                print('\nCet utilisateur existe déjà.\n')
                tools.prompt_ok()
            case _:
                print('Une erreur est survenue.')

    def success_msg(self, args):
        tools.clear_term()
        match args['type']:
            case 'user_logged':
                print('Bonjour, ' + args['user'].name)
            case 'new_user_created':
                print('Le collaborateur ' + args['user'].name + ' a été créé.')
        tools.prompt_ok()

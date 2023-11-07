from views import tools


class ReturnView:

    def welcome(self):
        tools.clear_term()
        msg = 'EpicEvents / Gestion de clientèle'
        content = msg.center(70, '*')
        print('\n')
        print(content)
        print('\n')

    def error_msg(self, error_type):
        match error_type:
            case 'bad_username':
                print('\nCet utilisateur n\'existe pas.\n')
            case 'bad_credentials':
                print('\nLe mot de passe et le nom d\'utilisateur ' +
                      'ne correspondent pas.\n')
            case 'existing_user':
                tools.clear_term()
                print('\nCet utilisateur existe déjà.\n')
                tools.prompt_ok()
            case 'self_deleting':
                tools.clear_term()
                print('\nVous ne pouvez pas vous supprimer vous-même.\n')
                tools.prompt_ok()
            case _:
                print('Une erreur est survenue.')

    def success_msg(self, args):
        tools.clear_term()
        match args['type']:
            case 'user_logged':
                msg = 'Bonjour, ' + args['user'].name
                print(tools.format_title(msg))
            case 'new_user_created':
                print('Le collaborateur ' + args['user'].name + ' a été créé.')
            case 'user_updated':
                print('Le collaborateur ' + args['user'].name +
                      ' a bien été modifié.')
            case 'user_deleted':
                print('Le collaborateur ' + args['user'] +
                      ' a bien été supprimé.')
        return tools.prompt_ok()

    def user_card(self, user):
        tools.clear_term()
        print(tools.format_title('Fiche collaborateur - ' + user.name))
        match user.role:
            case 'MAN':
                dept = 'Gestion'
            case 'COM':
                dept = 'Commercial'
            case 'SUP':
                dept = 'Support'

        args = [
            ['Nom:', user.name],
            ['Email:', user.email],
            ['Département:', dept],
            # ['Nom:'], [user.name],
        ]
        tools.display_table(args)
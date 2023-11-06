class ReturnView:

    def welcome(self):
        msg = 'EpicEvents / Gestion de clientèle'
        print(msg)

    def error_msg(self, error_type):
        match error_type:
            case 'bad_username':
                print('L\'utilisateur n\'existe pas.')
            case 'bad_credentials':
                print('Le mot de passe et le nom d\'utilisateur ' +
                      'ne correspondent pas.')
            case _:
                print('Une erreur est survenue.')
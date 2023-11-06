class FormView:
    def get_user_log_infos(self):
        credentials = {}
        credentials['username'] = input('Entrez votre nom d\'utilisateur:\n')
        credentials['password'] = input('Entrez votre mot de passe:\n')
        return credentials

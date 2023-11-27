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
                print('Création/modification impossible:')
                print('\nCet utilisateur existe déjà.\n')
                tools.prompt_ok()
            case 'self_deleting':
                tools.clear_term()
                print('Suppression impossible:')
                print('\nVous ne pouvez pas vous supprimer vous-même.\n')
                tools.prompt_ok()
            case 'existing_client':
                tools.clear_term()
                print('Création/modification impossible:')
                print('\nCe client existe déjà.\n')
                tools.prompt_ok()
            case 'existing_event':
                tools.clear_term()
                print('Création/modification impossible:')
                print('\nUn événement existe déjà pour ce contrat.\n')
                tools.prompt_ok()
            case _:
                print('Une erreur est survenue.')

    def success_msg(self, args):
        tools.clear_term()
        print(tools.format_title('Opération effectuée'))
        match args['type']:
            case 'user_logged':
                print('Bonjour, ' + args['user'].name)
            case 'new_user_created':
                print('Le collaborateur ' + args['user'].name + ' a été créé.')
            case 'user_updated':
                print('Le collaborateur ' + args['user'].name +
                      ' a bien été modifié.')
            case 'user_deleted':
                print('Le collaborateur ' + args['user'] +
                      ' a bien été supprimé.')
            case 'new_client_created':
                print('Le client ' + args['client'].name + ' a été créé.')
            case 'client_updated':
                print('Le client ' + args['client'].name +
                      ' a bien été modifié.')
            case 'client_deleted':
                print('Le client ' + args['client'] +
                      ' a bien été supprimé.')
            case 'new_contract_created':
                print('Le contract ' +
                      args['contract'].contract_name +
                      ' a été créé.')
            case 'contract_updated':
                print('Le contrat ' + args['contract'].contract_name +
                      ' a bien été modifié.')
            case 'event_updated':
                print('L\'événement ' + args['event'].name +
                      ' a bien été modifié.')

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

    def client_card(self, client):
        tools.clear_term()
        print(tools.format_title('Fiche client - ' + client.name))

        args = [
            ['Nom:', client.name],
            ['Email:', client.email],
            ['Téléphone:', client.phone],
            ['Entreprise:', client.company],
            ['Premier contact:', client.date_created],
            ['Dernier contact / mise à jour:', client.date_updated],
            ['Contact commercial:', client.epic_contact.name],
        ]
        tools.display_table(args)

    def contract_card(self, contract):
        tools.clear_term()
        print(tools.format_title('Fiche contrat - ' + contract.contract_name))

        args = [
            ['Client:', contract.client.name],
            ['Contrat signé:', 'Oui' if contract.signed else 'Non'],
            [
                'Coût total:',
                str(contract.total_amount) + ' euros' if
                contract.total_amount else
                'Non fourni'
            ],
            [
                'Montant dû:',
                str(contract.due_amount) + ' euros' if
                contract.due_amount else
                'Non fourni'
            ],
            ['Création contrat:', contract.date_created],
            ['Contact commercial:', contract.client.epic_contact.name],
        ]
        tools.display_table(args)

    def event_card(self, event):
        tools.clear_term()
        print(tools.format_title('Fiche événement - ' + event.name))

        args = [
            ['Nom:', event.name],
            ['Contrat:', event.contract.contract_name],
            ['Client:', event.contract.client.name],
            ['Date de début:', event.date_start],
            ['Date de fin:', event.date_end],
            ['Contact  chez Epic:', event.support.name],
            ['Lieu:', event.location],
            ['Nombre attendu:', event.attendees],
            ['Notes:', event.notes],
        ]
        tools.display_table(args)
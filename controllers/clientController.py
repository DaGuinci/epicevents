from models.models import Client


class ClientController():

    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.session = self.db_controller.session

    """
    Cclient creation:
    args.keys = [
    epic_contact
    name
    email
    phone
    company
    ]
    auto args = [
    date_created or date_updated
    ]
    """
    def create_client(self, args):
        client = (
            self.session.query(Client).
            filter(Client.name == args['name']).
            first()
            )
        if client and client.email == args['email']:
            return {
                'status': False,
                "error": 'existing_client'
                }
        else:
            new_client = Client(
                name=args['name'],
                email=args['email'],
                epic_contact=args['epic_contact'],
                phone=args['phone'],
                company=args['company'],
            )
            self.session.add(new_client)
            self.session.commit()
            client = (
                self.session.query(Client).
                filter(Client.name == args['name']).
                first()
                )
            if client:
                return {
                    'status': True,
                    'client': client
                    }

    # def get_user_clients(self, user):
    #     clients = (
    #         self.session.query(Client).
    #         filter(Client.epic_contact == user.user_id).
    #         all()
    #         )
    #     return clients

    def get_clients(self):
        clients = (
            self.session.query(Client).
            all()
            )
        return clients

    def update_client(self, client, key, value):
        match key:
            case 'name':
                clientname_exists = (
                    self.session.query(Client).
                    filter(client.name == value).
                    first()
                    )
                if (
                        clientname_exists and
                        clientname_exists.email == client.email
                        ):
                    return {
                        'status': False,
                        "error": 'existing_client'
                        }
                client.name = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'email':
                clientmail_exists = (
                    self.session.query(Client).
                    filter(client.email == value).
                    first()
                    )
                if clientmail_exists and clientmail_exists.name == client.name:
                    return {
                        'status': False,
                        "error": 'existing_client'
                        }
                else:
                    client.email = value
                    self.session.commit()
                    return {
                        'status': True,
                        }
            case 'phone':
                client.phone = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'company':
                client.company = value
                self.session.commit()
                return {
                    'status': True,
                    }

    def delete_client(self, client):
        self.session.delete(client)
        self.session.commit()
        return {
            'status': True,
            }
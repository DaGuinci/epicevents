from models.clientModel import Client


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
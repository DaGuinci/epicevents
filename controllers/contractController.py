from models.models import Contract, Client


class ContractController():

    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.session = self.db_controller.session

    """
    Contract creation:
    args.keys = [
    client
    total_amount
    due_amount
    signed
    date_created
    ]
    auto args = [
    date_created or date_updated
    ]
    """
    def create_contract(self, args):
        contracts = (
            self.session.query(Contract).
            filter(Contract.client == args['client']).
            all()
            )
        contract_name = (
            args['client'].company +
            '-' +
            str(len(contracts)+1)
            )
        new_contract = Contract(
            contract_name=contract_name,
            client=args['client'],
        )
        self.session.add(new_contract)
        self.session.commit()
        contract = (
            self.session.query(Contract).
            filter(Contract.contract_name == contract_name).
            first()
            )
        if contract:
            return {
                'status': True,
                'contract': contract
                }

    def get_contracts(self):
        contracts = (
            self.session.query(Contract).
            all()
            )
        return contracts

    def get_salesman_contracts(self, user):
        contracts = []
        clients = (
            self.session.query(Client).
            filter(Client.epic_contact == user).
            all()
        )
        if clients:
            for client in clients:
                client_contracts = (
                    self.session.query(Contract).
                    filter(Contract.client == client).
                    all()
                )
                contracts += client_contracts
        return contracts

    def get_salesman_signed_contracts(self, user):
        contracts = []
        clients = (
            self.session.query(Client).
            filter(Client.epic_contact == user).
            all()
        )
        if clients:
            for client in clients:
                client_contracts = (
                    self.session.query(Contract).
                    filter(Contract.client == client).
                    all()
                )
                if client_contracts:
                    for client_contract in client_contracts:
                        contracts.append((client_contract, client.name))
        return contracts

    def update_contract(self, contract, key, value):
        match key:
            case 'total_amount':
                contract.total_amount = round(value, 2)
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'due_amount':
                contract.due_amount = round(value, 2)
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'signed':
                contract.signed = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case _:
                return {
                    'status': False,
                    'error': 'generic'
                }

    def delete_contract(self, contract):
        self.session.delete(contract)
        self.session.commit()
        return {
            'status': True,
            }
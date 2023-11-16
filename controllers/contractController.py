from models.models import Contract


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
        contract_id = (
            args['client'].name +
            '-' +
            str(len(contracts)+1)
            )
        new_contract = Contract(
            contract_id=contract_id,
            client=args['client'],
        )
        self.session.add(new_contract)
        self.session.commit()
        contract = (
            self.session.query(Contract).
            filter(Contract.contract_id == contract_id).
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

    # def get_client_contracts(self, user):
    #     clients = (
    #         self.session.query(Client).
    #         filter(Client.epic_contact == user).
    #         all()
    #         )
    #     return clients

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
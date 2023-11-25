from models.models import Event, Contract


class EventController():

    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.session = self.db_controller.session

    def create_event(self, args):
        # Event already exists
        contract = (
            self.session.query(Contract).
            filter(Contract.contract_name == args['contract'].contract_name).
            first()
            )
        existing_event = (
            self.session.query(Event).
            filter(Event.contract_id == contract.contract_id).
            first()
            )
        if existing_event:
            return {
                'status': False,
                "error": 'existing_event'
                }
        new_event = Event(
            contract_id=args['contract'].contract_id,
            name=args['name'],
            epic_contact=args['epic_contact'].user_id,
            date_start=args['date_start'],
            date_end=args['date_end'],
            attendees=args['attendees'],
            notes=args['notes'],
        )
        self.session.add(new_event)
        self.session.commit()
        event = (
            self.session.query(Event).
            filter(Event.contract_id == args['contract'].contract_id).
            first()
            )
        if event:
            return {
                'status': True,
                'event': event
                }

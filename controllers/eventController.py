from models.models import Event, Contract, User


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

    def get_support_events(self, user):
        events = (
            self.session.query(Event).
            filter(Event.epic_contact == user.user_id).
            all()
            )
        for event in events:
            contract = (
                self.session.query(Contract).
                filter(Contract.contract_id == event.contract_id).
                first()
                )
            event.contract = contract
            support = (
                self.session.query(User).
                filter(User.user_id == event.epic_contact).
                first()
            )
            event.support = support
        return events

    def get_contract_event(self, contract):
        event = (
            self.session.query(Event).
            filter(Event.contract_id == contract.contract_id).
            first()
            )
        if event:
            return event
        return None

    def update_event(self, event, key, value):
        match key:
            case 'name':
                event.name = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'date_start':
                event.date_start = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'date_send':
                event.date_send = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'location':
                event.location = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'attendees':
                event.attendees = value
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'notes':
                event.notes = value
                self.session.commit()
                return {
                    'status': True,
                    }

    def delete_event(self, event):
        self.session.delete(event)
        self.session.commit()
        return {
            'status': True,
            }
from models.userModel import User
from passlib.hash import argon2
import secrets


class UserController():

    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.session = self.db_controller.session

    # login
    def login(self, log_infos):
        user = (
            self.session.query(User).
            filter(User.name == log_infos['username']).first()
            )
        if not user:
            return {
                'status': False,
                'error': 'bad_username'
                }
        else:
            # unsalt password
            hashed_stored = user.password[:-22]
            if argon2.verify(log_infos['password'], hashed_stored):
                return {
                'status': True,
                'user': user
                }
            else:
                return {
                'status': False,
                'error': 'bad_credentials'
                }

    def create_user(self, args):
        user = (
            self.session.query(User).filter(User.name == args['name']).first()
            )
        if user:
            return {
                'status': False,
                "error": 'existing_user'
                }
        else:
            # hash plaintext password
            hashed = argon2.hash(args['password'])
            # generate the salt\
            salt = secrets.token_urlsafe(16)
            # replace args password
            password = hashed + salt
            new_user = User(
                name=args['name'],
                email=args['email'],
                password=password,
                role=args['role']
            )
            self.session.add(new_user)
            self.session.commit()
            user = (
                self.session.query(User).
                filter(User.name == args['name']).
                first()
                )
            if user:
                return {
                    'status': True,
                    'user': user
                    }

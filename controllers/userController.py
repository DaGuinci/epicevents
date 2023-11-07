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
        if user and user.email == args['email']:
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

    def update_user(self, user, key, value):
        match key:
            case 'name':
                username_exists = (
                    self.session.query(User).
                    filter(User.name == value).
                    first()
                    )
                if username_exists and username_exists.email == user.email:
                    return {
                        'status': False,
                        "error": 'existing_user'
                        }
                else:
                    user.name = value
                    self.session.commit()
                    return {
                        'status': True,
                        }

            case 'password':
                # hash plaintext password
                hashed = argon2.hash(value)
                # generate the salt\
                salt = secrets.token_urlsafe(16)
                # replace args password
                password = hashed + salt
                user.password = password
                self.session.commit()
                return {
                    'status': True,
                    }
            case 'email':
                usermail_exists = (
                    self.session.query(User).
                    filter(User.email == value).
                    first()
                    )
                if usermail_exists and usermail_exists.name == user.name:
                    return {
                        'status': False,
                        "error": 'existing_user'
                        }
                else:
                    user.email = value
                    self.session.commit()
                    return {
                        'status': True,
                        }
            case 'role':
                user.role = value
                self.session.commit()
                return {
                    'status': True,
                    }

    def get_users(self):
        return (self.session.query(User).order_by(User.name))

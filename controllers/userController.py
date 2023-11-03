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
            return 'L\'utilisateur n\'existe pas.'
        else:
            # unsalt password
            hashed_stored = user.password[:-22]
            if argon2.verify(log_infos['password'], hashed_stored):
                return 'Utilisateur connecté.'
            else:
                return 'Connection echouée.'

    def create_user(self, args):
        user = (
            self.session.query(User).filter(User.name == args['name']).first()
            )
        if user:
            return ('Cet utilisateur existe déjà.')
        else:
            # hash plaintext password
            hashed = argon2.hash(args['password'])
            # generate the salt\
            salt = secrets.token_urlsafe(16)
            print(salt)
            # replace args password
            args['password'] = hashed + salt
            return self.db_controller.save_user(args)
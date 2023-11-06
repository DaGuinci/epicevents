import json
from controllers.mainController import MainController

# get the credential to connect to database
f = open('config.json')
config = json.load(f)
f.close()

# serve the credentials
db_credentials = config['db_config']

# No user connected
global _user
_user = None

main_controller = MainController(db_credentials)

# user = main_controller.user_controller.create_user({
#     'name': 'first_user3',
#     'email': 'first@user.com',
#     'password': 'userpass',
#     'role': 'SUP'
#     }
# )
# print(user)

# LIST ALL USERS
# users = data_controller.get_users()
# print(users)

# LOGIN
login_args = {
    'username': 'first_user3',
    'password': 'userpass'
}
# main_controller.user_controller.login(login_args)
# print(main_controller.logged)
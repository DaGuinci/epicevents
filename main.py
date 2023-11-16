import json
from controllers.mainController import MainController

# get the credential to connect to database
f = open('config.json')
config = json.load(f)
f.close()

# serve the credentials
db_credentials = config['db_config']

# No user connected

main_controller = MainController(db_credentials)
# main_controller.main_manager()
# user = main_controller.user_controller.create_user({
#     'name': 'manager',
#     'email': 'manage@user.com',
#     'password': 'userpass',
#     'role': 'MAN'
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
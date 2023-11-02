import json
from controllers.dbController import DataController

# get the credential to connect to database
f = open('config.json')
config = json.load(f)
f.close()

# serve the credentials
credentials = config['db_config']
data_controller = DataController(credentials)
user = data_controller.create_user({
    'name': 'first_user',
    'email': 'first@user.com',
    'password': 'userpass',
    'role': 'SUP'
    }
)

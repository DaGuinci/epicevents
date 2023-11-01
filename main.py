import json
from controllers.dbController import DataController

# get the credential to connect to database
f = open('config.json')
credentials = json.load(f)
f.close()

# serve the credentials
data_controller = DataController(credentials)
user = data_controller.get_user_by_name('first_user')
print('user 14:')
print(data_controller.get_user_by_id(14))
data_controller.delete_user(14)

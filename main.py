import json
from controllers.dbController import DataController

# get the credential to connect to database
f = open('config.json')
credentials = json.load(f)
f.close()

# serve the credentials
data_controller = DataController(credentials)
data_controller.read_datas()

import json

# import pymongo

# import datetime
# from pymongo import MongoClient

# host = "localhost"
# port = 27017

# username = "touch"
# password = "touchja"

# db_name = "mydb"  # database name to authenticate

# # if your password has '@' then you might need to escape hence we are using "urllib.parse.quote_plus()" 
# myclient = pymongo.MongoClient('mongodb://touch:touchja@localhost:27017/?authMechanism=DEFAULT') 

# mydb = myclient["dev"]
# mycol = mydb["sensor_data"]

# message = '{"espId" : 1, "temperature": 30, "humidity": 70}'
# json_data = json.loads(message)
# json_data['createAt'] = datetime.datetime.utcnow()
# print(json_data)
# print(type(json_data['temperature']))
# x = mycol.insert_one(json_data)
# print(x)

json_data = {'action': 'update/sensors', 'espId': 3, "temp": 27, 'humidity': '45.000000'}
input_data = {}
input_data['humidity'] = int(float(json_data['humidity']))
if(json_data.get('temps')):
    print('get')
print(input_data)
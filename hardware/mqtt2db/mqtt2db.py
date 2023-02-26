
import random

from paho.mqtt import client as mqtt_client

import json

import pymongo

import datetime

# move all variable to .env
broker = '192.168.2.45'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'admin'
password = 'password'
myclient = pymongo.MongoClient('mongodb://touch:touchja@localhost:27017/?authMechanism=DEFAULT') 

mydb = myclient["dev"]
mycol = mydb["sensor_data"]

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def save_data_to_mongo(json_data: json):
    # add more validation
    json_data['createAt'] = datetime.datetime.utcnow()
    x = mycol.insert_one(json_data)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        print(f"Received `{message}` from `{msg.topic}` topic")
        json_data = json.loads(message)
        save_data_to_mongo(json_data)
        
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
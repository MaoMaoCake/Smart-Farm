
import os
import random

from models import UpdateLightStrengthInput,UpdateAllSensorInput

from paho.mqtt import client as mqtt_client

import json

import pymongo

import datetime

from database.connector import update_light_strength_to_all_light,get_hardware_by_esp_id,get_farm_id_by_hardware_id,update_dehumidifier_status,update_co2_controller_status,update_all_sensor_data,get_threshold_by_farm_id,get_ac_status_by_farm_id,update_ac_status,get_dehumidifier_esp_id_by_esp_id,get_ac_esp_id_by_esp_id,get_co2_controller_esp_id_by_esp_id

from database.enum_list import System

from dotenv import load_dotenv
load_dotenv('mqtt2db.env')

broker = f"{os.getenv('MQTT_SERVER')}"
port = int(os.getenv('MQTT_PORT'))
topic = f"{os.getenv('MQTT_TOPIC')}"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = f"{os.getenv('MQTT_USERNAME')}"
password = f"{os.getenv('MQTT_PASSWORD')}"
myclient = pymongo.MongoClient("mongodb://"f"{os.getenv('MONGO_USERNAME')}"":"f"{os.getenv('MONGO_PASSWORD')}""@"f"{os.getenv('MONGO_SERVER')}"":"f"{os.getenv('MONGO_PORT')}""/?authMechanism=DEFAULT") 

mydb = myclient[f"{os.getenv('MONGO_DB')}"]
mycol = mydb[f"{os.getenv('MONGO_COLLECTION')}"]

def connect_mqtt() -> mqtt_client:
    try:
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
    except:
        print("[connect_mqtt] cannot connect to the mqtt broker")

client = connect_mqtt()

def publish_data(client: mqtt_client,topic: str, data: json):
    try:
        def on_publish(client,userdata,result):             #create function for callback
            print("data published \n")
            pass
        client.on_publish = on_publish
        ret= client.publish(topic,data)
    except:
        print("[publish_data] cannot publish the data to the mqtt")

def get_farm_id_by_esp_id(esp_id: int):
    try:
        hardware = get_hardware_by_esp_id(esp_id)
        farm_id = get_farm_id_by_hardware_id(hardware["hardware_id"],hardware["hardware_type"])
        return farm_id
    except:
        print("[get_farm_id_by_esp_id] cannot get the farm id from espId:", esp_id)

def update_light(esp_id: int, json_data: json):
    try:
        updateInput = UpdateLightStrengthInput(json_data['natural_percent'],json_data['uv_percent'],json_data['ir_percent'])
        farm_id = get_farm_id_by_esp_id(esp_id)
        update_light_strength_to_all_light(updateInput,farm_id,System.USERNAME.value)
    except:
        print("[update_light] cannot update light status with the espId:", esp_id, "and data:", json_data)

def update_dehumidifier(esp_id: int, json_data: json):
    try:
        farm_id = get_farm_id_by_esp_id(esp_id)
        update_dehumidifier_status(bool(json_data['activate']),farm_id,System.USERNAME.value)
    except:
        print("[update_light] cannot update light status with the espId:", esp_id, "and data:", json_data)

def update_co2_controller(esp_id: int, json_data: json):
    try:
        farm_id = get_farm_id_by_esp_id(esp_id)
        update_co2_controller_status(bool(json_data['activate']),farm_id,System.USERNAME.value)
    except:
        print("[update_light] cannot update light status with the espId:", esp_id, "and data:", json_data)

def update_all_sensor_data_to_sql(farm_id: int, esp_id: int, json_data: json):
    try:
        updatInput = UpdateAllSensorInput(json_data['temperature'],json_data['humidity'],json_data['co2'])
        update_all_sensor_data(updatInput,farm_id,System.USERNAME.value)
    except:
        print("[update_light] cannot update light status with the espId:", esp_id, "and data:", json_data)

def get_threshold(esp_id: int):
    try:
        farm_id = get_farm_id_by_esp_id(esp_id)
        threshold = get_threshold_by_farm_id(farm_id)
        return threshold
    except:
        print("[get_threshold] cannot get the co2 and humidity thresholds from mysql for espId:", esp_id)

def get_ac_status(esp_id: int):
    try:
        farm_id = get_farm_id_by_esp_id(esp_id)
        ac_status = get_ac_status_by_farm_id(farm_id)
        return ac_status
    except:
        print("[get_ac_status] cannot get the ac status from mysql for espId:", esp_id)

def send_threshold(esp_id: int):
    try:
        threshold = get_threshold(esp_id)
        ret = publish_data(client,str(esp_id),json.dumps(threshold))
    except:
        print("[send_threshold] cannot send the co2 and humidity thresholds to the espId:", esp_id)

def send_ac_status(esp_id: int):
    try:
        ac_status = get_ac_status(esp_id)
        ret = publish_data(client,str(esp_id),json.dumps(ac_status))
    except:
        print("[send_ac_status] cannot send the ac status to initiate the ac to the espId:", esp_id)

def turn_on_dehumidifier(esp_id: int):
    try:
        esp_ids = get_dehumidifier_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            dehumidifier_command = {}
            dehumidifier_command['activate'] = True
            ret = publish_data(client,str(i),json.dumps(dehumidifier_command))
    except:
        print("[turn_on_dehumidifier] cannot turn on the dehumidifier with espId:", esp_id)

def turn_off_dehumidifier(esp_id: int):
    try:
        esp_ids = get_dehumidifier_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            dehumidifier_command = {}
            dehumidifier_command['activate'] = False
            ret = publish_data(client,str(i),json.dumps(dehumidifier_command))
    except:
        print("[turn_off_dehumidifier] cannot turn off the dehumidifier with espId:", esp_id)

def turn_on_ac(esp_id: int):
    try:
        esp_ids = get_ac_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            ac_command = {}
            ac_command['activate'] = True
            ac_command['temperature'] = 14
            ret = publish_data(client,str(i),json.dumps(ac_command))    
    except:
        print("[turn_on_ac]: cannot turn on the ac with espId:", esp_id)

def turn_off_ac(esp_id: int):
    try:
        esp_ids = get_ac_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            ac_command = {}
            ac_command['activate'] = False
            ret = publish_data(client,str(i),json.dumps(ac_command))    
    except:
        print("[turn_off_ac]: cannot turn off the ac with espId:", esp_id)

def turn_on_co2(esp_id: int):
    try:
        esp_ids = get_co2_controller_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            co2_command = {}
            co2_command['activate'] = False
            ret = publish_data(client,str(i),json.dumps(co2_command))  
    except:
        print("[turn_on_co2] cannot turn on the co2 controller with espId:", esp_id)

def turn_off_co2(esp_id: int):
    try:
        esp_ids = get_co2_controller_esp_id_by_esp_id(esp_id)
        for i in esp_ids:
            co2_command = {}
            co2_command['activate'] = False
            ret = publish_data(client,str(i),json.dumps(co2_command))
    except:
        print("[turn_off_co2] cannot turn off the co2 controller with espId:", esp_id)

def update_ac(esp_id: int,json_data: json):
    try:
        farm_id = get_farm_id_by_esp_id(esp_id)
        update_ac_status(json_data['ac_status'],json_data['temperature'],farm_id,System.USERNAME.value)
    except:
        print("[update_ac] cannot update the ac data into mysql with espId:", esp_id, "and data:", json_data)

def switch(json_data: json):
    try:
        action = str(json_data['action'])
        esp_id = int(json_data['espId'])
        print('espId',esp_id)
        match action:
            case "update/light":
                print("update/light")
                update_light(esp_id, json_data)
            case "update/dehumidifier":
                update_dehumidifier(esp_id, json_data)
            case "update/co2":
                update_co2_controller(esp_id, json_data)
            case "update/sensors":
                farm_id = get_farm_id_by_esp_id(esp_id)
                save_data_to_mongo(farm_id,json_data)
                update_all_sensor_data_to_sql(farm_id,esp_id, json_data)
            case "get/threshold":
                send_threshold(esp_id)
            case "get/ac_status":
                send_ac_status(esp_id)
            case "update/ac_status":
                update_ac(esp_id,json_data)
            case "turn_on/dehumidifier":
                turn_on_dehumidifier(esp_id)
                turn_on_ac(esp_id)
            case "turn_off/dehumidifier":
                turn_off_dehumidifier(esp_id)
                turn_off_ac(esp_id)
            case "turn_on/co2":
                turn_on_co2(esp_id)
            case "turn_off/co2":
                turn_off_co2(esp_id)
    except:
        print("[switch] cannot take the action from the mqtt payload with data:", json_data)

def save_data_to_mongo(farm_id: int,json_data: json):
    try:
        currentDateTime = datetime.datetime.utcnow()
        createdMinute = (currentDateTime.minute//5)*5
        createdDateTime = datetime.datetime(currentDateTime.year,currentDateTime.month,currentDateTime.day,currentDateTime.hour,createdMinute)
        json_data['farmId'] = farm_id
        json_data['createAt'] = createdDateTime
        x = mycol.insert_one(json_data)
    except:
        print("[save_data_to_mongo] cannot save the data into the mongoDB with farm_id:", farm_id, "and data:", json_data)

def subscribe(client: mqtt_client):
    try:
        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            print(f"Received `{message}` from `{msg.topic}` topic")
            json_data = json.loads(message)

            switch(json_data)
            
        client.subscribe(topic)
        client.on_message = on_message
    except:
        print("[subscribe] cannot subcribe the mqtt with client:", client)

def run():
    try:
        subscribe(client)
        client.loop_forever()
    except:
        print("[run] cannot run the mqtt2db / cannot run the mqtt client")


if __name__ == '__main__':
    run()
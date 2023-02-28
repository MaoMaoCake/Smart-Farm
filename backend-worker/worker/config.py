import os
import requests

url = os.environ.get("MQTT_BRIDGE_URL")
headers = {"Content-Type": "application/json"}
key = os.environ.get("MQTT_BRIDGE_KEY")


def create_mqtt_request(topic: str, message: str) -> requests.Response:
    payload = {
        "topic": topic,
        "message": message,
        "key": key
    }

    return requests.request("POST", url, json=payload, headers=headers)

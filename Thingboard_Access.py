import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import ADC0832
import math
import json

THINGSBOARD_HOST = '4.206.153.143'
ACCESS_TOKEN = 'kNEETOZLfd70XMNaPOKO'
TOPIC = "v1/devices/me/telemetry"

def init():
    global client
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()

def pub(message):
    client.publish(TOPIC, json.dumps(message), 1)
    print(f"send {message} to ${TOPIC}")

def exit():
    client.loop_stop()
    client.disconnect()
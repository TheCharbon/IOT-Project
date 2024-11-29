import paho.mqtt.client as mqtt
import time
import ADC0832
import RPi.GPIO as GPIO
import json
import distance_sens
import soilMoisture
import thermores
import fan
import LEDs
import RGB_led
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
ACCESS_TOKEN = "sYlvPrNVobW2p2EpJObK"
THINGSBOARD_HOST = "4.206.153.143"

#Global power
light_power = False
fan_power = False
pump_power = False

#overwrites
light_overwrite = False
fan_overwrite = False
pump_overwrite = False

light_threshold = 1
moisture_threshold = 0
tempature_treshold = 0

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('v1/devices/me/rpc/request/+')
    print(f"Connected with result code {rc}")
    


client = mqtt.Client()
client.loop_start()
client.on_connect = on_connect

client.username_pw_set(ACCESS_TOKEN)


# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
collected_data = {
    "temperature" : "INIT",
    "moisture" : "INIT",
    "distance" : "INIT"
    }
def send(data):
    client.publish('v1/devices/me/telemetry', json.dumps(collected_data), 1)
    print(f"send {data} to v1/devices/me/telemetry")
def on_message(client, userdata, msg):
    global fan_overwrite, light_overwrite, pump_overwrite
    print("Got message")
    print(msg.payload)
    payload = json.loads(msg.payload.decode('utf-8'))
    if "method" in payload and "params" in payload:
        method = payload["method"]
        params = payload["params"]
        if method == "setFanState":
            if params == True:
                print("Fan on")
                fan_overwrite = True
                fan.power_on()
            else:
                print("Fan off")
                fan_overwrite = False
                fan.power_off()
        elif method == "setLightState":
            if params == True:
                print("Lights on")
                light_overwrite = True
                LEDs.red_on()
                LEDs.blue_on()
            else:
                print("Fan off")
                light_overwrite = False
                LEDs.blue_off()
                LEDs.red_off()
        elif method == "setPumpState":
            if params == True:
                print("Pump on")
                pump_overwrite = True
                RGB_led.setColor("GREEN")

            else:
                print("Pump off")
                pump_overwrite = False
                RGB_led.setColor("RED")






client.on_message = on_message


def init():
    ADC0832.setup()
    distance_sens.init()
    soilMoisture.init()
    thermores.init()
    fan.init()
    LEDs.init()
    RGB_led.init()
    global myMQTTClient
    myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
    myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
    myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
    myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
    myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
    if myMQTTClient.connect():
        print('AWS connection succeeded')
def pub(message):
    myMQTTClient.publish(config.TOPIC, message, 1)
    print(f"send {message} to ${config.TOPIC}")
def loop():
    global pump_overwrite, fan_overwrite, light_overwrite
    while True:
        collected_data["distance"] = distance_sens.checkdist()
        collected_data["moisture"] = soilMoisture.get_reading()
        collected_data["temperature"] = thermores.read_temp()

        if collected_data["distance"] <= 1 and not light_overwrite:
            LEDs.blue_on()
            LEDs.red_on()
        elif collected_data["distance"] >= 1 and not light_overwrite:
            LEDs.blue_off()
            LEDs.red_off()

        if collected_data["moisture"] <= moisture_threshold and not pump_overwrite:
            RGB_led.setColor("GREEN")
        elif collected_data["moisture"] >= moisture_threshold and not pump_overwrite:
            RGB_led.setColor("RED")

        if float(collected_data["temperature"]) >= tempature_treshold and not fan_overwrite:
            fan.power_on()
        elif float(collected_data["temperature"]) <= tempature_treshold and not fan_overwrite:
            fan.power_off()

        json_data = json.dumps(collected_data)
        send(json_data)
        pub(json_data)
        time.sleep(5)

if __name__ == '__main__':
    init()
    print("Welcome to the smart greehouse system!")
    print("Type help for a list of commands")
    try:
        while True:
            user_in = input("Smart Greenhouse-> ")
            if user_in == "temp":
                while True:
                    print("enter a temperature or back")
                    user_in = input("Smart Greenhouse Temp-> ")
                    if float(user_in):
                        tempature_treshold = float(user_in)
                        print("Temperature Set!")
                        break
                    elif user_in == "back":
                        break
                    else:
                        print("Invalid command")
            elif user_in == "moisture":
                while True:
                    print("enter a mosture value or back")
                    user_in = input("Smart Greenhouse Moisture-> ")
                    if float(user_in):
                        moisture_threshold = float(user_in)
                        print("Moisture set!")
                        break
                    elif user_in == "back":
                        break
                    else:
                        print("Invalid command")
            elif user_in == "start":
                try:
                    loop()
                except KeyboardInterrupt:
                    ADC0832.destroy()
                    break
    except KeyboardInterrupt:
        print("Application Terminated")
        ADC0832.destroy()
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import ADC0832
import math
import json

THINGSBOARD_HOST = '4.206.153.143'
ACCESS_TOKEN = 'kNEETOZLfd70XMNaPOKO'
TOPIC = "v1/devices/me/telemetry"

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)


# Send message to host
def pub(message):
    client.publish(TOPIC, json.dumps(message), 1)
    print(f"send {message} to ${TOPIC}")

def loop():
    while True:
        try:
            res0 = ADC0832.getADC(0)
            kel = 1/((1/298.15) + (1/3380) * math.log((255/res0) - 1))
            cel = float(kel - 273.15)
            res1 = ADC0832.getADC(1)
            brightness = ""
            if (res1 > 128):
                    brightness = "light"
            else:
                    brightness = "dark"

            obj = {
                "Celsius": str(round(cel, 2)),
                "Brightness": brightness
            }
            pub(obj)
            time.sleep(1)
        except():
            time.sleep(1)
            print("skipped")

def init():
    ADC0832.setup()
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        client.loop_stop()
        client.disconnect()
        print ('The end !')
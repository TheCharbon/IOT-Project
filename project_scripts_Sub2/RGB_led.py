import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import ADC0832
import json
import time

pins = {
    "R": 13, 
    "G": 12, 
    "B": 16
}

colors = {
    "RED": 0xFF0000,
    "GREEN": 0x00FF00
}

def init():
    for i in pins:
        gpio.setup(pins[i], gpio.OUT)
        gpio.output(pins[i], gpio.HIGH)
    global p_R
    global p_G
    global p_B
    for i in pins:
        gpio.setup(pins[i], gpio.OUT)
    p_R = gpio.PWM(pins['R'], 2000)
    p_G = gpio.PWM(pins['G'], 2000)
    p_B = gpio.PWM(pins['B'], 5000)

    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(input):
    if input == "GREEN" or input == "GREEN":
        col = colors[input]
        print(col)
    else:
        return
    R_val = (col & 0xFF0000) >> 16
    G_val = (col & 0x00FF00) >> 8
    B_val = (col & 0x0000FF) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    print(R_val,G_val,B_val)
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)




def exit():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    for i in pins:
        gpio.output(pins[i], gpio.HIGH)
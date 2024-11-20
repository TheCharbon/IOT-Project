import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import ADC0832
import json
import time

pins = {
    "R": 21, 
    "G": 20, 
    "B": 16
}

colors = {
    "RED": "FF0000",
    "GREEN": "0000FF"
}

def init():
    global p_R
    global p_G
    global p_B
    p_R = gpio.PWM(pins['pin_R'], 2000)
    p_G = gpio.PWM(pins['pin_G'], 2000)
    p_B = gpio.PWM(pins['pin_B'], 5000)

    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(input):
    if input == "GREEN" or input == "RED":
        col = colors[input]
    else:
        return
    R_val = (col & 0x110000) >> 16
    G_val = (col & 0x001100) >> 8
    B_val = (col & 0x000011) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)

def exit():
    p_R.stop()
    p_G.stop()
    p_B.stop()
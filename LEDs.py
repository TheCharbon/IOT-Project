import RPi.GPIO as gpio

pins = {
    "red_led": 26,
    "blue_led": 19
}

def init():
    gpio.setmode(gpio.BCM)
    for i in pins:
        gpio.setup(pins[i], gpio.OUT)

def red_on():
    gpio.output(pins["red_led"], gpio.HIGH)

def red_off():
    gpio.output(pins["red_led"], gpio.LOW)

def blue_on():
    gpio.output(pins["blue_led"], gpio.HIGH)

def blue_off():
    gpio.output(pins["blue_led"], gpio.LOW)

def exit():
    gpio.cleanup()
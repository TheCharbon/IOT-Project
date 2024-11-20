import RPi.GPIO as gpio

button_pin = 13

def init():
    gpio.setmode(gpio.BCM)
    gpio.add_event_detect(button_pin, gpio.FALLING, callback=on_button_pressed, bouncetime=300)

def on_button_pressed():
    pass # do something

def exit():
    gpio.cleanup()
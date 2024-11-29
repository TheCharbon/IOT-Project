import RPi.GPIO as gpio

button_pin = 23

def init():

    gpio.setmode(gpio.BCM)
    gpio.setup(button_pin, gpio.IN)
    gpio.add_event_detect(button_pin, gpio.FALLING, callback=on_button_pressed, bouncetime=300)

def on_button_pressed():
    print("Button Pressed!")

def exit():
    gpio.cleanup()
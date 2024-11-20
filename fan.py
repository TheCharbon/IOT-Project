import RPi.GPIO as GPIO
import time
power_pin = 12
powered = False
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_pin,  GPIO.OUT)

def power_on():
    global powered
    if not powered:
        GPIO.output(power_pin, True)
        powered = True

def power_off():
    global powered
    if powered:
        GPIO.output(power_pin, False)
        powered = False


def destroy():
    GPIO.output(power_pin, False)

if __name__ == '__main__':
    init()
    power_on()
    time.sleep(5)
    destroy()
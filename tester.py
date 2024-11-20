import ADC0832 as ADC0832
import thermores
import fan 
import time
import soilMoisture
import RPi.GPIO as GPIO
def init():
    GPIO.setmode(GPIO.BCM)
    ADC0832.setup()
    fan.init()
def destroy():
    ADC0832.destroy()
    fan.destroy()
if __name__ == '__main__':
    init()
    fan.power_on()
    time.sleep(5)
    print()
    print(soilMoisture.get_reading())
    print(thermores.read_temp())
    destroy()

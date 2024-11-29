import ADC0832 as ADC0832
import thermores
import fan 
import time
import soilMoisture
import RPi.GPIO as GPIO
import LEDs
import RGB_led
import distance_sens

def init():
    GPIO.setmode(GPIO.BCM)
    ADC0832.setup()
    fan.init()
    LEDs.init()
    RGB_led.init()
    distance_sens.init()

def destroy():
    ADC0832.destroy()
    #fan.destroy()
    #LEDs.blue_off()
    #LEDs.red_off()
    #RGB_led.exit()
if __name__ == '__main__':
    init()
    RGB_led.setColor("GREEN")
    LEDs.red_on()
    LEDs.blue_on()
    fan.power_on()
    time.sleep(5)
    #print(distance_sens.checkdist())
    print(soilMoisture.get_reading())
    print(thermores.read_temp())
    destroy()

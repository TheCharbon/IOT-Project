#!/usr/bin/env python
import ADC0832 as ADC0832
import time
import math
def init():
    ADC0832.setup()
def loop():
    while True:
        res = ADC0832.getADC(0)
        if res == 0:
            print("Somthing Went Wrong: 0 Division found trying again...")
            continue
        Vr = 3.3 * float(res) / 255
        if Vr == 3.3:
            print("Somthing Went Wrong: 0 Division found trying again...")
            continue
        Rt = 10000 * Vr / (3.3 - Vr)
            #print('Rt : %.2f' % Rt)
       
        celciusTemp = float
        farenheightTemp = float
        kelvenTemp = float


        kelvenTemp = 1/298.15 + 1/3455 * math.log((255 / res) - 1)

        kelvenTemp = 1/kelvenTemp
        celciusTemp = kelvenTemp - 273.15
        farenheightTemp = (celciusTemp * 9/5) +32

        #Discard Garbage Values
        if celciusTemp >= 50 or celciusTemp<= -50:
            print("Outlier, Descarded value")
        else:
            print("--------------------------------------------")
            print(str(round(celciusTemp,2)) + "°C", "    ", str(round(farenheightTemp,2)) + "°F")
        time.sleep(0.2)

def read_temp():
    res = ADC0832.getADC(0)
    if res == 0:
        return("ERROR")
    Vr = 3.3 * float(res) / 255
    if Vr == 3.3:
        return("ERROR") 
    celciusTemp = float
    kelvenTemp = float
    kelvenTemp = 1/298.15 + 1/3455 * math.log((255 / res) - 1)
    kelvenTemp = 1/kelvenTemp
    celciusTemp = kelvenTemp - 273.15
    #Discard Garbage Values
    if celciusTemp >= 50 or celciusTemp<= -50:
         return("Outlier Value")
    else:
        return celciusTemp
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print('The end!')


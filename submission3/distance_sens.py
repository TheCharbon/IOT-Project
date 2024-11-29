import RPi.GPIO as GPIO
import time
import ADC0832 as ADC0832
trig = 20
echo = 21
def init():
    ADC0832.setup()
    GPIO.setup(trig,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo,GPIO.IN)
	
def checkdist():
	GPIO.output(trig, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(trig, GPIO.LOW)
	while not GPIO.input(echo):
		pass
	t1 = time.time()
	while GPIO.input(echo):
		pass
	t2 = time.time()
	return (t2-t1)*340/2
def loop():
      while True:
            print(checkdist())
            time.sleep(0.5)
            
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print('The end!')
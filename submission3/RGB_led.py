import RPi.GPIO as gpio

pins = {
    "R": 13, 
    "G": 12, 
}

def init():
    for i in pins:
        gpio.setup(pins[i], gpio.OUT)
        gpio.output(pins[i], gpio.HIGH)
    global p_R
    global p_G
    for i in pins:
        gpio.setup(pins[i], gpio.OUT)
    p_R = gpio.PWM(pins['R'], 100)
    p_G = gpio.PWM(pins['G'], 100)

    p_R.start(100)
    p_G.start(100)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(input):
    if input == "GREEN":
        p_R.ChangeDutyCycle(100)
        p_G.ChangeDutyCycle(0)
    elif input == "RED":
        p_R.ChangeDutyCycle(0)
        p_G.ChangeDutyCycle(100)

def exit():
    p_R.stop()
    p_G.stop()
    for i in pins:
        gpio.output(pins[i], gpio.HIGH)
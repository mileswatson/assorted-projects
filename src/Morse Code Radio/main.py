
from time import time
import RPi.GPIO as GPIO

class translate:

    dictionary = {"a":[0,1],"b":[1,0,0,0],"c":[1,0,1,0],"d":[1,0,0],"e":[0],"f":[0,0,1,0],"g":[1,1,0],"h":[0,0,0,0],"i":[0,0],"j":[0,1,1,1],"k":[1,0,1],"l":[0,1,0,0],"m":[1,1],"n":[1,0],"o":[1,1,1],"p":[0,1,1,0],"q":[1,1,0,1],"r":[0,1,0],"s":[0,0,0],"t":[1],"u":[0,0,1],"v":[0,0,0,1],"w":[0,1,1],"x":[1,0,0,1],"y":[1,0,1,1],"z":[1,1,0,0],"1":[0,1,1,1,1],"2":[0,0,1,1,1],"3":[0,0,0,1,1],"4":[0,0,0,0,1],"5":[0,0,0,0,0],"6":[1,0,0,0,0],"7":[1,1,0,0,0],"8":[1,1,1,0,0],"9":[1,1,1,1,0],"0":[1,1,1,1,1]}

    def toMorse(self,string):
        returnList = []
        for char in string.lower():
            if char in translate.dictionary:
                returnList += self.numParse(translate.dictionary[char])
            else:
                returnList += [0 for i in range(15)]
        return returnList

    def numParse(self,array):
        returnList = []
        for number in array:
            if number == 0:
                returnList += [0,1,0]
            elif number == 1:
                returnList += [1,1,0]
        returnList += [0 for i in range(15-len(returnList))]
        return returnList

class radio:

    def __init__(self,cps,op,recv=False,lpin=15):
        
        self.tp = 1/(cps*15)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(op, GPIO.OUT)
        GPIO.setup(lpin,GPIO.OUT)
        self.led = GPIO.PWM(lpin,500)
        self.led.start(0)
        self.op = op

    def broadcast(self,array):
        timeit = time()
        print("start")
        waitUntil = time() + (self.tp*15)
        GPIO.output(self.op,1)
        self.led.ChangeDutyCycle(100)
        while waitUntil > time():
            pass
        GPIO.output(self.op,0)
        self.led.ChangeDutyCycle(0)
        waitUntil += (self.tp*15)
        while waitUntil > time():
            pass
        for number in array:
            waitUntil += self.tp
            GPIO.output(self.op,number)
            self.led.ChangeDutyCycle(100*number)
            while time() < waitUntil:
                pass
        waitUntil += (self.tp*15)
        GPIO.output(self.op,0)
        self.led.ChangeDutyCycle(0)
        while waitUntil > time():
            pass
        GPIO.output(self.op,1)
        self.led.ChangeDutyCycle(100)
        waitUntil += (self.tp*15)
        while waitUntil > time():
            pass
        GPIO.output(self.op,0)
        self.led.ChangeDutyCycle(0)
        print("done")
        print("estimated",((time()-timeit)/(self.tp*15))-4,"letters transmitted.")

translator = translate()

transmit = radio(float(input("How many letters per second would you like to send?\n")),17)

while True:
    array = translator.toMorse(input("What would you like to send as morse code?\n"))
    transmit.broadcast(array)
    
simulate = False

if simulate:
    import SimulRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO
import threading
import time
from enum import Enum
from threading import Event, Thread

class BoardType(Enum):
    BOARD = 0
    BCM = 1

class Distance():
    def __init__(self, triggerPin, echoPin, gpioPinRef: BoardType):
        self._triggerPin = triggerPin
        self._echoPin = echoPin
        if gpioPinRef == BoardType.BCM:
            GPIO.setmode(GPIO.BCM)
        elif gpioPinRef == BoardType.BOARD:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._triggerPin, GPIO.OUT)
        GPIO.setup(self._echoPin, GPIO.IN)  
                
    def distance(self, measure='cm'):
        try:           
            GPIO.output(self._triggerPin, True)     
            time.sleep(0.00001)
            GPIO.output(self._triggerPin, False)
            
            while GPIO.input(self._echoPin) == 0:
                startTime = time.time()

            while GPIO.input(self._echoPin) == 1:
                endTime = time.time()

            elapsed = endTime - startTime

            if measure == 'cm':
                distance = elapsed / 0.000058
            elif measure == 'in':
                distance = elapsed / 0.000148
            else:
                print('improper choice of measurement: in or cm')
                distance = None

            
            #GPIO.cleanup()
            return distance
        except:
            print('in exception')
            distance = 100
            GPIO.cleanup()
            return distance

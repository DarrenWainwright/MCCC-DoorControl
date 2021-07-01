simulate = False

from threading import Event, Thread
import threading
from enum import Enum
import time
from SimulRPi.GPIO import BCM
if simulate:
    import SimulRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO



# motor class
# ctor take in gpio pins and type
# function forward(maxTime) runs the motor until a maximum time in seconds. use 0 to run indefinitely
# function backward(maxTime) same as above
# function stop() stops motor

class BoardType(Enum):
    BOARD = 0
    BCM = 1

class Motor(threading.Thread):
    def __init__(self, pwma, ain1, ain2, stby, gpioPinRef: BoardType): 
        threading.Thread.__init__(self)  
        print('motor2')
        self._pwma = pwma
        self._ain1 = ain1
        self._ain2 = ain2
        self._stby = stby
        if gpioPinRef == BoardType.BCM:
            GPIO.setmode(GPIO.BCM)
        elif gpioPinRef == BoardType.BOARD:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BOARD)
        #self._SetPinState(True)
        #GPIO.cleanup()     



    def _SetPinState(self, state: any):          
        GPIO.setup(self._pwma, state) # Connected to PWMA
        GPIO.setup(self._ain1, state) # Connected to AIN1
        GPIO.setup(self._ain2, state) # Connected to AIN2
        GPIO.setup(self._stby, state) # Connected to STBY

    def _RunMotor(self, clockwise: bool):
        if clockwise == True:
            print("Running clockwise")
            # Drive the motor clockwise
            GPIO.output(self._ain1, GPIO.HIGH) # Set AIN1
            GPIO.output(self._ain2, GPIO.LOW) # Set AIN2
        else:
            print("Running counter clockwise")
             # Drive the motor clockwise
            GPIO.output(self._ain1, GPIO.LOW) # Set AIN1
            GPIO.output(self._ain2, GPIO.HIGH) # Set AIN2

        # Set the motor speed
        GPIO.output(self._pwma, GPIO.HIGH) # Set PWMA

        # Disable STBY (standby)
        GPIO.output(self._stby, GPIO.HIGH)

    # maxTime to run the motor in seconds
    def forward(self, maxTime: int):
        print("Start motor running forward")
        self._SetPinState(GPIO.OUT)
        self._RunMotor(True)
        Event.wait(maxTime)
        #time.sleep(maxTime)
        self.stop()
      
    def backward(self, maxTime: int):
        self._SetPinState(False)
        self._RunMotor(False)
        Event.wait(maxTime)
        #time.sleep(maxTime)
        self.stop()

    def stop(self):
        self._SetPinState(GPIO.LOW)
        GPIO.cleanup()

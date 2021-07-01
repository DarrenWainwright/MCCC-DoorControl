simulate = False

from enum import Enum
from Distance import Distance
import time
from SimulRPi.GPIO import BCM
if simulate:
    import SimulRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()


class BoardType(Enum):
    BOARD = 0
    BCM = 1

class SimpleDoor():
    def __init__(self): 
        self._pwma = int(os.getenv("MOTOR_PWMA"))
        self._ain1 = int(os.getenv("MOTOR_AIN1"))
        self._ain2 = int(os.getenv("MOTOR_AIN2"))
        self._stby = int(os.getenv("MOTOR_STBY"))
        self._distanceClosed = int(os.getenv("DISTANCE_WHEN_CLOSED"))
        self._distanceOpened = int(os.getenv("DISTANCE_WHEN_OPEN"))
        self._boardType = os.getenv("BOARD_TYPE")
        self._distance = Distance(int(os.getenv("DISTANCE_TRIGGER")), int(os.getenv("DISTANCE_ECHO")), self._boardType)

    def _SetPinState(self, state: any):       
        if self._boardType == BoardType.BCM:
            GPIO.setmode(GPIO.BCM)
        elif self._boardType == BoardType.BOARD:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BOARD)   
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
    def open(self, maxTime: int):
        print("Start motor running forward")
        started = time.time()
        distance = self._distance.distance('in')
        self._SetPinState(GPIO.OUT)
        self._RunMotor(True)
        opened = False
        while not (opened == True):
            runtime = time.time() - started
            distance = self._distance.distance('in')   
            print("Runtime:" + str(runtime)) 
            print("Distance:" + str(distance))                              
            if (runtime >= maxTime ):
                print('runtime greater than max, stopping')
                self.stop()
                opened = True
            if (distance >= self._distanceOpened):
                print('reached door opening position, stopping')
                self.stop()
                opened = True  
            time.sleep(1)   
        
      
    def close(self, maxTime: int):
        print("Start motor running forward")
        started = time.time()
        distance = self._distance.distance('in')
        self._SetPinState(GPIO.OUT)
        self._RunMotor(False)
        opened = False
        while not (opened == True):
            runtime = time.time() - started
            distance = self._distance.distance('in')   
            print("Runtime:" + str(runtime)) 
            print("Distance:" + str(distance))                              
            if (runtime >= maxTime ):
                print('runtime greater than max, stopping')
                self.stop()
                opened = True
            if (distance <= self._distanceClosed):
                print('reached door closed position, stopping')
                self.stop()
                opened = True  
            time.sleep(1)   

    def stop(self):
        self._SetPinState(GPIO.LOW)
        GPIO.cleanup()

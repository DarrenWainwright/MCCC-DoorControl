from Motor import Motor
from Distance import Distance
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

triggerPin = int(os.getenv("DISTANCE_TRIGGER"))
echoPin = int(os.getenv("DISTANCE_ECHO"))
boardType = os.getenv("BOARD_TYPE")
pwma = int(os.getenv("MOTOR_PWMA"))
ain1 = int(os.getenv("MOTOR_AIN1"))
ain2 = int(os.getenv("MOTOR_AIN2"))
stby = int(os.getenv("MOTOR_STBY"))

class Door:

    def  __init__(self, maxMotorRuntime, distanceWhenOpen, distanceWhenClosed) -> None:
        self._maxMotorRuntime = maxMotorRuntime
        self._distanceWhenOpen = distanceWhenOpen
        self._distanceWhenClosed = distanceWhenClosed
        self._distance = Distance(triggerPin, echoPin, boardType)
        self._motor = Motor(pwma, ain1, ain2, stby, boardType)
        self._motor.start()
        #self._distance.start()

    def _WithinMargin(self, distance, comparedTo) -> bool:
        # % margin of error on distance
        margin = 10
        diff = abs(distance - comparedTo)
        percent = (diff / distance) * 100
        return percent <= margin

    def open(self) -> bool:
        print("Open door..")
        start = self._distance.distance("in")
        print("current door position: " + str(start))
        if (self._WithinMargin(start, self._distanceWhenClosed)):
            current = start
            print("Door position: " + str(current))
            print(current <= self._distanceWhenOpen)
            self._motor.forward(self._maxMotorRuntime)
            print("motor running")
            while current <= self._distanceWhenOpen:                
                current = self._distance.distance("in")
                print("Door position: " + str(current))  
            print('call stop')
            self._motor.stop()
        else:
            print("Door appears to be already open")
        return True
        
            
    def close(self):
        start = self._distance.distance("in")
        if (self._WithinMargin(start, self._distanceWhenOpen)):
            current = start
            print("Door position: " + current)
            while current <= self._distanceWhenClosed:
                self._motor.backward(self._maxMotorRuntime)
                current = self._distance.distance("in")
                print("Door position: " + current)
        else:
            print("Door appears to be already closed")
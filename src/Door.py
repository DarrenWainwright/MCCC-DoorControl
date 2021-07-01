from Motor import Motor
from Distance import Distance


class Door:

    def  __init__(self, maxMotorRuntime, distanceWhenOpen, distanceWhenClosed) -> None:
        self._maxMotorRuntime = maxMotorRuntime
        self._distanceWhenOpen = distanceWhenOpen
        self._distanceWhenClosed = distanceWhenClosed
        self._distance = Distance()
        self._motor = Motor()
        self._motor.start()
        self._motor.start()

    def _WithinMargin(self, distance, comparedTo) -> bool:
        # % margin of error on distance
        margin = 10
        diff = abs(distance - comparedTo)
        percent = (diff / distance) * 100
        return percent <= margin

    def open(self) -> bool:
        print("Open door..")
        start = self._distance.distance("in")
        if (self._WithinMargin(start, self._distanceWhenClosed)):
            current = start
            print("Door position: " + current)
            while current <= self._distanceWhenOpen:
                self._motor.forward(self._maxMotorRuntime)
                current = self._distance.distance("in")
                print("Door position: " + current)            
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
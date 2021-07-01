from SimpleDoor import SimpleDoor

door = SimpleDoor()
door.open(30)


# from SimulRPi.GPIO import BOARD
# from dotenv import load_dotenv
# from Motor import BoardType, Motor
# from Distance import Distance
# from Door import Door
# import time
# import os
# import RPi.GPIO as GPIO

# GPIO.cleanup()

# # Load env vars
# load_dotenv()

# triggerPin = int(os.getenv("DISTANCE_TRIGGER"))
# echoPin = int(os.getenv("DISTANCE_ECHO"))
# boardType = os.getenv("BOARD_TYPE")
# pwma = int(os.getenv("MOTOR_PWMA"))
# ain1 = int(os.getenv("MOTOR_AIN1"))
# ain2 = int(os.getenv("MOTOR_AIN2"))
# stby = int(os.getenv("MOTOR_STBY"))

# motor = Motor(1,2,3,4,BOARD)
# motor.stop()
# # door = Door(5, 25, 1)
# # door.open()

# # switch = False
# # state = "x" if switch == True else "Y";  
# # print(state)
# #motor = Motor(7, 12, 11, 13, BoardType.BOARD)
# # motor.forward(1.5)

# # print(os.environ.get('USER'))
# triggerPin = int(os.getenv("DISTANCE_TRIGGER"))
# echoPin = int(os.getenv("DISTANCE_ECHO"))
# boardType = os.getenv("BOARD_TYPE")

# # distance = Distance(triggerPin, echoPin, boardType)

# # while True:
# #     d = distance.distance('in')
# #     print(d)
# #     time.sleep(1)




# # GPIO.setmode(GPIO.BOARD)

# # # set up GPIO pins
# # GPIO.setup(7, GPIO.OUT) # Connected to PWMA
# # GPIO.setup(11, GPIO.OUT) # Connected to AIN2
# # GPIO.setup(12, GPIO.OUT) # Connected to AIN1
# # GPIO.setup(13, GPIO.OUT) # Connected to STBY
# # print("bla")
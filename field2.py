from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
# declare sensors + motors
RMotor = Motor("A")
LMotor = Motor("B")
motor_pair = MotorPair("B", "A")

RColor = ColorSensor("D")
LColor = ColorSensor("C")
ultrasonic = DistanceSensor("F")
enterZone = False
GrabMotor = Motor("E")
#Line Tracing function
angle = hub.motion_sensor.get_yaw_angle() - 90
if angle <= -180:
    angle = 180 - abs(angle - -180)
RSpeed = 16
LSpeed = 16
bumpCount = 0
boxPos = 0
posOne = 0
posTwo = 0
countOne = 0
countTwo = 0
temp = 0
def trace():
    global distance
    global extra
    RValue = RColor.get_color()
    LValue = LColor.get_color()
    if RValue == None and LValue == "white":
        motor_pair.start_tank(LSpeed, RSpeed)
        wait_for_seconds(0.7)
        motor_pair.start_tank(0, 0)
        wait_for_seconds(0.2)
        motor_pair.start_tank(-40, 40)
        wait_for_seconds(0.55)
        motor_pair.start_tank(20, 20)
        wait_for_seconds(0.4)
    elif RValue == "white" and LValue == None:
        motor_pair.start_tank(LSpeed, RSpeed)
        wait_for_seconds(0.7)
        motor_pair.start_tank(0, 0)
        wait_for_seconds(0.2)
        motor_pair.start_tank(40, -40)
        wait_for_seconds(0.55)
        motor_pair.start_tank(20, 20)
        wait_for_seconds(0.4)
    elif RValue == "white" and LValue == "white":
        motor_pair.start_tank(LSpeed, RSpeed)
    elif RValue == "black" and LValue == "white":
        motor_pair.start_tank(-20, 40)
    elif RValue == "white" and LValue == "black":
        motor_pair.start_tank(40, -20)

    if hub.motion_sensor.was_gesture('shaken'):
        motor_pair.start_tank(-40, -40)
        wait_for_seconds(0.5)
        motor_pair.start_tank(100, 100)
        wait_for_seconds(1.5)
        motor_pair.start_tank(0, 0)
        wait_for_seconds(0.5)
        motor_pair.start_tank(40, -40)
        wait_for_seconds(0.8)
        motor_pair.start_tank(0, 0)
        wait_for_seconds(1)
        motor_pair.start_tank(LSpeed, RSpeed)

    extra = ultrasonic.get_distance_cm()
    if extra != None:
        distance = extra
        if distance <= 8 and hub.motion_sensor.get_yaw_angle()< angle + 45 and hub.motion_sensor.get_yaw_angle() > angle - 45:
            motor_pair.start_tank(0, 0)
            motor_pair.start_tank(-40, -40)
            motor_pair.start_tank(40, -40)
            wait_for_seconds(0.6)
            motor_pair.start_tank(LSpeed, RSpeed)
            wait_for_seconds(3)
            motor_pair.start_tank(-40, 40)
            wait_for_seconds(0.60)
            motor_pair.start_tank(LSpeed, RSpeed)
            wait_for_seconds(8)
            motor_pair.start_tank(-40, 40)
            wait_for_seconds(0.6)
            motor_pair.start_tank(LSpeed, RSpeed)
            wait_for_seconds(3)
            motor_pair.start_tank(40, -40)
            wait_for_seconds(0.6)


    # print(hub.motion_sensor.get_pitch_angle())
    # if hub.motion_sensor.get_pitch_angle() >= 4 or hub.motion_sensor.get_pitch_angle() <= -4:
    #    if bumpCount == 1:
    #        motor_pair.start_tank(24, 24)
    #        wait_for_seconds(0.3)
    #        motor_pair.start_tank(-40, 40)
    #        wait_for_seconds(0.55)
    #        motor_pair.start_tank(24, 24)
    #    else:
    #        bumpCount += 1
    #        wait_for_seconds(0.5)

# find box position
def findBox():
    global posOne
    global posTwo
    global countOne
    global countTwo
    global temp
    motor_pair.start_tank(40, 0)
    wait_for_seconds(0.5)
    motor_pair.start_tank(10, 10)
    wait_for_seconds(0.5)
    motor_pair.start_tank(0, 40)
    wait_for_seconds(0.5)
    motor_pair.start_tank(0, 0)
    for x in range (20):
        temp = ultrasonic.get_distance_cm()
        if type(temp) is int:
            posOne += temp
            countOne += 1
        if countOne == 0:
            countOne = 1
    wait_for_seconds(0.5)
    motor_pair.start_tank(-40, -40)
    wait_for_seconds(0.6)
    motor_pair.start_tank(-40, 40)
    wait_for_seconds(0.7)
    motor_pair.start_tank(0, 0)
    for x in range (20):
        temp = ultrasonic.get_distance_cm()
        if type(temp) is int:
            posTwo += temp
            countTwo += 1
        if countTwo == 0:
            countTwo = 1

#Main Tracing Loop:
while enterZone == False:
    if RColor.get_color() == "red" or LColor.get_color() == "red":
        enterZone = True
    else:
        motor_pair.start_tank(LSpeed, RSpeed)
motor_pair.start_tank(40, 40)
wait_for_seconds(1)
motor_pair.start_tank(0, 0)
findBox()
print(posOne/countOne)
print(posTwo/countTwo)
if posOne / countOne >= 55 and posOne / countOne <= 85:
    motor_pair.start_tank(-40, 40)
    wait_for_seconds(0.525)
    motor_pair.start_tank(-60, -60)
    wait_for_seconds(2.7)
    motor_pair.start_tank(0, 0)
    wait_for_seconds(0.5)
    motor_pair.start_tank(60, 60)
    wait_for_seconds(1)
    motor_pair.start_tank(0, 0)
elif posTwo / countTwo >= 50 and posTwo / countTwo <= 90:
    motor_pair.start_tank(-40, 40)
    wait_for_seconds(1.1)
    motor_pair.start_tank(-80, -80)
    wait_for_seconds(1.5)
    motor_pair.start_tank(0, 0)
    wait_for_seconds(1)
    motor_pair.start_tank(60, 60)
    wait_for_seconds(1)
    motor_pair.start_tank(0, 0)
else:
    motor_pair.start_tank(-40, 40)
    wait_for_seconds(0.735)
    motor_pair.start_tank(-80, -80)
    wait_for_seconds(2.7)
    motor_pair.start_tank(0, 0)
    wait_for_seconds(1)
    motor_pair.start_tank(60, 60)
    wait_for_seconds(1)
    motor_pair.start_tank(0, 0)

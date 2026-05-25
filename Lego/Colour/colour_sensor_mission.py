#!/usr/bin/env pybricks-micropython
"""
Demonstrates interactive Color Sensor calibration and implements a basic 
Proportional (P) control loop to follow the edge of a line.
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

lift_motor = Motor(Port.A)

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# The ColorSensor outputs a reflection value between 0 (dark) and 100 (light).
line_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, 56, 121)

def move(distance):
    """
    Move the robot in a straight line and then pause.

    Parameters:
        distance (int): The distance to move in millimetres.
                        A positive value moves forward.
                        A negative value moves backward.
        pause (int):    The time to wait after the movement, in milliseconds.

    This function is useful because it groups two common actions:
    1. move the robot,
    2. pause so that the movement can be observed clearly.
    """
    # Move the robot straight for the given distance.
    robot.straight(distance)

# =============================================================================
# CALIBRATION LOGIC
# =============================================================================

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on BLACK")
ev3.screen.draw_text(0, 50, "Press any btn")

while len(ev3.buttons.pressed()) == 0:
    wait(10)
    
black_value = line_sensor.reflection()

ev3.speaker.beep(500, 200)

while len(ev3.buttons.pressed()) > 0:
    wait(10)

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")

while len(ev3.buttons.pressed()) == 0:
    wait(10)
    
white_value = line_sensor.reflection()

ev3.speaker.beep(1000, 200)

while len(ev3.buttons.pressed()) > 0:
    wait(10)

TARGET_THRESHOLD = (black_value + white_value) / 2

ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))

print("Calibration Complete. Threshold:", TARGET_THRESHOLD)
wait(3000) 

# =============================================================================
# PROPORTIONAL (P) CONTROL LOOP WITH TURNS
# =============================================================================

DRIVE_SPEED = 100       
PROPORTIONAL_GAIN = 1.2 

ev3.speaker.beep()
ev3.screen.clear()

# Reset distance counter
robot.reset()

# === Segment 1: Drive 300mm while following line ===

while robot.distance() < 500:
    current_reflection = line_sensor.reflection()
    error = current_reflection - TARGET_THRESHOLD
    steering = error * PROPORTIONAL_GAIN
    robot.drive(DRIVE_SPEED, steering)
    wait(10)

# Stop and turn right 90 degrees
robot.stop()
robot.turn(90)
wait(500)

# Reset distance counter for next segment
robot.reset()

# === Segment 2: Drive another 300mm while following line ===
while robot.distance() < 600:
    current_reflection = line_sensor.reflection()
    error = current_reflection - TARGET_THRESHOLD
    steering = error * PROPORTIONAL_GAIN
    robot.drive(DRIVE_SPEED, steering)
    wait(10)

# Stop and turn left 90 degrees
robot.stop()
robot.turn(-90)
wait(500)

# === Segment 3: Drive straight (NO line following) ===
robot.reset()

# Just drive straight without using the sensor

lift_motor.run_target(200, 40) #raise arm
move(40)
wait(100)
lift_motor.run_target(100, -10) #lower arm
move(-25)
wait(100)
lift_motor.run_target(200, 40) #raise arm
robot.turn(90)
move(400)
robot.turn(45)
move(550)

# Stop at the end
robot.stop()
ev3.speaker.beep(2000, 500)
ev3.screen.clear()
ev3.screen.draw_text(0, 50, "Mission Complete!")
ev3.screen.draw_text(0, 70, "Press button to exit")

# Wait for button press before ending
while len(ev3.buttons.pressed()) == 0:
    wait(10)
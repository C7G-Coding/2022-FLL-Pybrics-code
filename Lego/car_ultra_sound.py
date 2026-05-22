#!/usr/bin/env pybricks-micropython

"""
Turbine and Car Mission
=========================
1. Move straight 70 cm
2. Turn right 20 degrees
3. Do the following 4 times:
      - Move forward 10 cm
      - Move backward 5 cm
4. Wait 5 seconds
5. Move backward 10 cm
6. Turn left 90 degrees
7. Move forward 20 cm
8. Raise arm high
9. Wait 5 seconds
10. Move backward 50 cm
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --------------------------------------------------
# Hardware setup
# --------------------------------------------------

# Import the EV3Brick class.
# This gives us access to the EV3 brick itself, including features such
# as the speaker, buttons, and screen.
from pybricks.hubs import EV3Brick

# Import the Motor class so that we can create motor objects for the
# left and right wheels of the robot.
# Import the UltrasonicSensor class so that we can create an object
# representing the ultrasonic sensor connected to the EV3.
from pybricks.ev3devices import Motor, UltrasonicSensor

# Import Port so that we can refer to the physical ports on the EV3
# brick, such as motor ports B and C, and sensor port S4.
from pybricks.parameters import Port

# Import DriveBase, which makes it easier to control a two-wheel robot.
# Instead of controlling each motor separately all the time, we can use
# higher-level movement commands such as drive(), straight(), and turn().
from pybricks.robotics import DriveBase

# Import wait so that we can pause the program for a specified number
# of milliseconds. This is useful when we want the robot to stop briefly
# before continuing with the next action.
from pybricks.tools import wait


# Create an EV3Brick object.
# This represents the EV3 brick and allows us to use built-in features
# such as the speaker for beeps.
ev3 = EV3Brick()

# Create the motor object for the left wheel.
# The motor is connected to Port B on the EV3.
left_motor = Motor(Port.B)

# Create the motor object for the right wheel.
# The motor is connected to Port C on the EV3.
right_motor = Motor(Port.C)

# Create a DriveBase object.
# A DriveBase combines the two drive motors into a robot that can move
# forward, backward, and turn.
#
# wheel_diameter is the diameter of the wheels in millimetres.
# axle_track is the distance between the centres of the two wheels.
#
# These measurements are important because they affect the accuracy of
# the robot's movement.
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=118)

# Create the ultrasonic sensor object.
# This tells the program that an ultrasonic sensor is connected to
# sensor Port S4.
ultrasonic = UltrasonicSensor(Port.S2)

ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor  = Motor(Port.A)   # Arm control

# Robot measurements (adjust if needed)
wheel_diameter = 56
axle_track = 123               # You can use 121 if that's your exact robot

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def move(distance_mm):
    """Move straight: positive = forward, negative = backward."""
    robot.straight(distance_mm)

def turn(angle):
    """Turn in place: positive = left, negative = right."""
    robot.turn(angle)

def arm_up():
    """Raise the arm to its high position."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)   # Up angle (adjust if needed)
    wait(500)

def arm_down():
    """Lower the arm (not used here, but available)."""
    lift_motor.run_target(100, -5)
    wait(520)

# --------------------------------------------------
# Main mission function
# --------------------------------------------------
def turbine_and_car_mission():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Turbine & Car")

    # 1. Move straight 70 cm (700 mm)
    move(470)

    # # 2. Turn right 20 degrees
    # turn(46)

    # # 3. Do the next two steps 4 times:
    # for _ in range(4):
    #     move(100)   # forward 10 cm
    #     move(-50)   # backward 5 cm

    # # 4. Wait for 5 seconds
    wait(200)

    # 5. Move backward 10 cm
    # move(-150)

    # 6. Turn left 90 degrees
    turn(-47)

    # 7. Move forward 20 cm
    move(380)

    # 8. Raise arm high
    arm_up()
    arm_down()

    # 9. Wait 5 seconds
    wait(200)

    # 10. Move backward 50 cm
    move(-700)

    # Optional: sound to mark completion
    ev3.speaker.beep(1000, 300)
    ev3.screen.clear()

# --------------------------------------------------
# Run the mission when the file is executed
# --------------------------------------------------
if __name__ == "__main__":
    turbine_and_car_mission()
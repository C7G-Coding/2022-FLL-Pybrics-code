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
    wait(500)

# --------------------------------------------------
# Main mission function
# --------------------------------------------------
def turbine_and_car_mission():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Turbine & Car")

    # 1. Move straight 70 cm (700 mm)
    move(650)

    # 2. Turn right 20 degrees
    turn(46)

    # 3. Do the next two steps 4 times:
    for _ in range(4):
        move(100)   # forward 10 cm
        move(-50)   # backward 5 cm

    # 4. Wait for 5 seconds
    wait(2000)

    # 5. Move backward 10 cm
    turn(-46)

    # 6. Turn left 90 degrees
   
    move(-600)

    # Optional: sound to mark completion
    ev3.speaker.beep(1000, 300)
    ev3.screen.clear()

# --------------------------------------------------
# Run the mission when the file is executed
# --------------------------------------------------
if __name__ == "__main__":
    turbine_and_car_mission()
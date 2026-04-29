#!/usr/bin/env pybricks-micropython

"""
Mission 1 - FIRST LEGO League 2022
======================================
Movement plan:
  1. Raise arm to starting position (up)
  2. Drive forward 460 mm (46 cm)
  3. Drop the arm down to complete the pickup
  4. Stay in place (no return)
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --------------------------------------------------
# Device setup
# --------------------------------------------------

ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor  = Motor(Port.A)

WHEEL_DIAMETER = 56
AXLE_TRACK     = 123

robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def move(distance_mm):
    """Drive straight. Positive = forward, negative = backward."""
    robot.straight(distance_mm)
    wait(300)

def arm_up():
    """Raise the arm to the up position (matches raise.py exactly)."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)
    wait(500)

def arm_down():
    """Lower the arm to the down position (matches lower.py exactly)."""
    lift_motor.run_target(100, -110)
    wait(500)

# --------------------------------------------------
# Mission 1
# --------------------------------------------------

def main():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Mission 1")
    ev3.speaker.beep()
    wait(500)

    # Step 1 - Raise arm before driving
    arm_up()

    # Step 2 - Drive forward 46 cm to reach the model
    move(460)

    # Step 3 - Drop the arm to complete the action
    arm_down()

    # Done - robot stays here
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")

if __name__ == "__main__":
    main()

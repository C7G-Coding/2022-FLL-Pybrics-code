#!/usr/bin/env pybricks-micropython

"""
Mission 1 - FIRST LEGO League 2022
======================================
Movement plan:
  1. Drive forward 460 mm (46 cm)
  2. Lower arm to pick up the model
  3. Raise arm to secure the model
  4. Drive backward 460 mm (46 cm) to return to base
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
lift_motor  = Motor(Port.A)   # Attachment / pickup arm

# --------------------------------------------------
# Robot measurements  (match your robot exactly)
# --------------------------------------------------

WHEEL_DIAMETER = 56    # mm
AXLE_TRACK     = 123   # mm  (centre-to-centre of wheels)

robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def move(distance_mm):
    """Drive straight. Positive = forward, negative = backward."""
    robot.straight(distance_mm)
    wait(300)


def pickup():
    """
    Lower the arm onto the model, then raise it to secure it.
    Adjust the target angles to match your physical attachment.
    """
    # Lower arm to floor level
    lift_motor.run_target(150, -90)   # -90 deg = arm down
    wait(400)

    # Raise arm to carry position
    lift_motor.run_target(150, 0)     # 0 deg   = arm up
    wait(400)


# --------------------------------------------------
# Mission
# --------------------------------------------------

def main():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Mission 1")
    ev3.speaker.beep()
    wait(500)

    # Step 1 – Drive forward to the model (46 cm)
    move(460)

    # Step 2 – Pick up the model
    pickup()

    # Step 3 – Drive backward to return to base (same 46 cm)
    move(-460)

    # Done!
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")


if __name__ == "__main__":
    main()

#!/usr/bin/env pybricks-micropython

"""
Mission 3 - FIRST LEGO League 2022
======================================
Base route (shared with Mission 2):
  1.  16.5 cm straight
  2.  17 cm curving right
  3.  Turn left 30 degrees
  4.  30 cm straight
  5.  Left curve 20 degrees
  6.  21 cm straight
  7.  Turn right 90 degrees
  8.  60 cm straight  <-- arrives at mission area

Mission 3 specific:
  9.  Turn around 270 degrees (clockwise / right)
  10. Drive forward 21 cm
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

def turn(angle_deg):
    """
    Turn in place.
    Positive = left (counter-clockwise).
    Negative = right (clockwise).
    """
    robot.turn(angle_deg)
    wait(300)

def curve(distance_mm, steering):
    """
    Drive an arc for a set distance.
    steering > 0 curves left, steering < 0 curves right.
    Uses time-based loop at 200 mm/s.
    """
    duration_ms = int(abs(distance_mm / 200) * 1000)
    elapsed = 0
    while elapsed < duration_ms:
        robot.drive(200, steering)
        wait(10)
        elapsed += 10
    robot.stop()
    wait(300)

# --------------------------------------------------
# Shared base route
# --------------------------------------------------

def run_base_route():
    """Drive from home base to the mission area."""

    # 1. 16.5 cm straight
    move(165)

    # 2. 17 cm curving right
    curve(170, -20)

    # 3. Turn left 30 degrees
    turn(30)

    # 4. 30 cm straight
    move(300)

    # 5. Left curve 20 degrees
    curve(80, 20)

    # 6. 21 cm straight
    move(210)

    # 7. Turn right 90 degrees
    turn(-90)

    # 8. 60 cm straight to reach mission area
    move(600)

# --------------------------------------------------
# Mission 3
# --------------------------------------------------

def main():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Mission 3")
    ev3.speaker.beep()
    wait(500)

    # Drive to mission area using shared base route
    run_base_route()

    # Step 9 - Turn 270 degrees clockwise (right = negative in Pybricks)
    # Pybricks robot.turn() handles large angles correctly in one call,
    # just like turn_360.py demonstrates with 360-degree turns.
    turn(-270)

    # Step 10 - Drive forward 21 cm
    move(210)

    # Done
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")

if __name__ == "__main__":
    main()

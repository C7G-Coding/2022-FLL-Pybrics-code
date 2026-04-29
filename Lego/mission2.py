#!/usr/bin/env pybricks-micropython

"""
Mission 2 - FIRST LEGO League 2022
======================================
Base route (shared with Mission 3):
  1.  16.5 cm straight
  2.  17 cm curving right
  3.  Turn left 30 degrees
  4.  30 cm straight
  5.  Left curve 20 degrees
  6.  21 cm straight
  7.  Turn right 90 degrees
  8.  60 cm straight  <-- arrives at mission area

Mission 2 specific:
  9.  Turn left 90 degrees
  10. Drive forward 11 cm
  11. Lower arm
  12. Drive backward 3 cm at full power to pull
  13. Raise arm
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

def arm_up():
    """Raise the arm (matches raise.py exactly)."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)
    wait(500)

def arm_down():
    """Lower the arm (matches lower.py exactly)."""
    lift_motor.run_target(100, -110)
    wait(500)

def pull_back(distance_mm):
    """
    Reverse at maximum motor speed to pull the model.
    Drives both motors directly at full speed for a calculated duration.
    At ~900 deg/s with a 56mm wheel: linear speed ≈ 440 mm/s
    """
    robot.stop()
    # 900 deg/s is near the EV3 large motor maximum
    pull_speed_mm_per_s = 440
    duration_ms = int((distance_mm / pull_speed_mm_per_s) * 1000)
    left_motor.run(-900)
    right_motor.run(-900)
    wait(duration_ms)
    left_motor.brake()
    right_motor.brake()
    wait(400)

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

    # 5. Left curve 20 degrees (short arc to nudge direction)
    curve(80, 20)

    # 6. 21 cm straight
    move(210)

    # 7. Turn right 90 degrees
    turn(-90)

    # 8. 60 cm straight to reach mission area
    move(600)

# --------------------------------------------------
# Mission 2
# --------------------------------------------------

def main():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Mission 2")
    ev3.speaker.beep()
    wait(500)

    # Drive to mission area using shared base route
    run_base_route()

    # Step 9 - Turn left 90 degrees to face mission model
    turn(90)

    # Step 10 - Drive forward 11 cm toward the model
    move(110)

    # Step 11 - Lower arm onto the model
    arm_down()

    # Step 12 - Pull back 3 cm at full motor power
    pull_back(30)

    # Step 13 - Raise arm
    arm_up()

    # Done
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")

if __name__ == "__main__":
    main()

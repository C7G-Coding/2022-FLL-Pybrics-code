#!/usr/bin/env pybricks-micropython

"""
Mission 3 - FIRST LEGO League 2022
======================================
Base route (shared with Mission 2):
  1.  16.5 cm straight
  2.  17 cm, curve right
  3.  Turn left 30 degrees
  4.  30 cm straight
  5.  Left curve 20 degrees  (OR follow black line with colour sensor)
  6.  21 cm straight
  7.  Turn right 90 degrees
  8.  60 cm straight   <-- arrives at mission area

Mission 3 specific steps:
  9.  Turn around 270 degrees (clockwise = right)
  10. Drive forward 21 cm to complete the mission
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
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
line_sensor = ColorSensor(Port.S3)

WHEEL_DIAMETER = 56
AXLE_TRACK     = 123

robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def move(distance_mm, speed=200):
    """Drive straight. Positive = forward, negative = backward."""
    robot.settings(straight_speed=speed)
    robot.straight(distance_mm)
    robot.settings(straight_speed=200)
    wait(300)


def turn(angle_deg):
    """
    Turn in place.
    Positive angle = LEFT turn.
    Negative angle = RIGHT turn.
    """
    robot.turn(angle_deg)
    wait(300)


def curve(distance_mm, steering_deg):
    """
    Drive an arc.
    steering_deg > 0  curves left.
    steering_deg < 0  curves right.
    Duration is calculated from distance and a fixed speed of 200 mm/s.
    """
    duration_ms = int(abs(distance_mm / 200) * 1000)
    elapsed = 0
    while elapsed < duration_ms:
        robot.drive(200, steering_deg)
        wait(10)
        elapsed += 10
    robot.stop()
    wait(300)


def follow_line_distance(distance_mm, threshold=50, speed=100, gain=1.2):
    """
    Follow the edge of a black line for a set distance using the colour sensor.
    threshold: midpoint between your black and white calibration readings.
               Change this value to match your mat conditions.
    """
    duration_ms = int(abs(distance_mm / speed) * 1000)
    elapsed = 0
    while elapsed < duration_ms:
        reflection = line_sensor.reflection()
        error      = reflection - threshold
        steering   = error * gain
        robot.drive(speed, steering)
        wait(10)
        elapsed += 10
    robot.stop()
    wait(300)


# --------------------------------------------------
# Shared base route
# --------------------------------------------------

def run_base_route():
    """
    Drive from home base to the mission area.
    Shared with Mission 2.
    """
    # 1. 16.5 cm straight
    move(165)

    # 2. 17 cm curving to the right (mild right arc)
    curve(170, -15)

    # 3. Turn left 30 degrees
    turn(30)

    # 4. 30 cm straight
    # -- Option A: plain straight drive --
    move(300)

    # -- Option B: colour-sensor line follow (uncomment & remove steps 4-5)
    # follow_line_distance(300 + 210, threshold=50)

    # 5. Left curve 20 degrees
    curve(50, 20)

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

    # --- Drive to mission area ---
    run_base_route()

    # Step 9 – Turn around 270 degrees clockwise (right turn = negative)
    # A 270-degree right turn is equivalent to a 90-degree left turn in
    # terms of final heading, but follows the longer arc as required.
    # Split into two movements so the robot pivots cleanly.
    turn(-270)

    # Step 10 – Drive forward 21 cm to complete the mission
    move(210)

    # Done!
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")


if __name__ == "__main__":
    main()

#!/usr/bin/env pybricks-micropython

"""
Mission 2 - FIRST LEGO League 2022
======================================
Base route (shared with Mission 3):
  1.  16.5 cm straight
  2.  17 cm, curve right
  3.  Turn left 30 degrees
  4.  30 cm straight
  5.  Left curve 20 degrees  (OR follow black line with colour sensor)
  6.  21 cm straight
  7.  Turn right 90 degrees
  8.  60 cm straight   <-- arrives at mission area

Mission 2 specific steps:
  9.  Turn left 90 degrees
  10. Drive forward 11 cm
  11. Lower arm onto target
  12. Drive backward 3 cm at FULL motor power to pull the model
  13. Raise arm
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
    robot.settings(straight_speed=200)   # restore default
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


def arm_down():
    """Lower the arm onto the mission model."""
    lift_motor.run_target(150, -90)   # adjust angle to match your attachment
    wait(400)


def arm_up():
    """Raise the arm back up."""
    lift_motor.run_target(150, 0)
    wait(400)


def pull_back(distance_mm=30):
    """
    Reverse at maximum motor speed to pull the model.
    Uses the raw motors directly so we can force 100 % duty cycle.
    """
    robot.stop()
    # Run both drive motors backwards at full speed
    left_motor.run(-900)    # 900 deg/s is near the EV3 motor maximum
    right_motor.run(-900)
    # Calculate how long to run: distance / (speed in mm/s)
    # At 900 deg/s with a 56 mm wheel: speed ≈ 900 * π * 56 / 360 ≈ 440 mm/s
    pull_duration_ms = int((distance_mm / 440) * 1000)
    wait(pull_duration_ms)
    left_motor.stop()
    right_motor.stop()
    wait(400)


# --------------------------------------------------
# Shared base route
# --------------------------------------------------

def run_base_route():
    """
    Drive from home base to the mission area.
    Shared with Mission 3.
    """
    # 1. 16.5 cm straight
    move(165)

    # 2. 17 cm curving to the right (mild right arc)
    curve(170, -15)          # steering -15 gives a gentle right curve

    # 3. Turn left 30 degrees
    turn(30)

    # 4. 30 cm straight
    # -- Option A: plain straight drive (comment out option B below) --
    move(300)

    # -- Option B: follow black line instead of steps 4-5
    # Uncomment the two lines below and comment out steps 4 and 5 if
    # you want to use the colour sensor from here to the 21 cm mark.
    # follow_line_distance(300 + 210, threshold=50)

    # 5. Left curve 20 degrees (gentle left arc over a short distance)
    curve(50, 20)             # 5 cm arc to nudge left 20 degrees

    # 6. 21 cm straight
    move(210)

    # 7. Turn right 90 degrees  (negative = right in Pybricks)
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

    # --- Drive to mission area ---
    run_base_route()

    # Step 9 – Turn left 90 degrees to face the mission model
    turn(90)

    # Step 10 – Drive forward 11 cm toward the model
    move(110)

    # Step 11 – Lower arm onto the model
    arm_down()

    # Step 12 – Pull back 3 cm at full power
    pull_back(30)

    # Step 13 – Raise arm
    arm_up()

    # Done!
    ev3.speaker.beep(1000, 500)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Done!")


if __name__ == "__main__":
    main()

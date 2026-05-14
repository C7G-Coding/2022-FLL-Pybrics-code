#!/usr/bin/env pybricks-micropython

"""
Line Follower – Stay on Black (Port S3)
========================================
Calibrates the colour sensor on the black line,
then follows the black line (not the edge) by steering
back toward black whenever the sensor sees white.

Built from the custom movement routine structure.
"""

# --------------------------------------------------
# Imports (same style as your original)
# --------------------------------------------------
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port

# Lift motor (if used later)
lift_motor = Motor(Port.A)

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

# Colour sensor on Port S3
color_sensor = ColorSensor(Port.S3)

# --------------------------------------------------
# Robot measurements
# --------------------------------------------------
wheel_diameter = 56
axle_track = 123

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions (your original style)
# --------------------------------------------------
def move(distance):
    robot.straight(distance)
    print("Moving", distance, "mm")

def turn(angle):
    robot.turn(angle)
    print("Turning", angle, "degrees")

def pause(ms=2000):
    wait(ms)
    print("Pausing", ms, "milliseconds")

def celebrate():
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()

# --------------------------------------------------
# Calibration – record the black line value
# --------------------------------------------------
def calibrate_black():
    global BLACK_THRESHOLD
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK LINE")
    ev3.screen.draw_text(0, 50, "Press any btn")

    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    black_value = color_sensor.reflection()
    ev3.speaker.beep(500, 200)

    while len(ev3.buttons.pressed()) > 0:
        wait(10)

    # Set threshold just above the black reading
    # so we can tell when we drift onto white.
    BLACK_THRESHOLD = black_value + 15   # 15 gives a safe margin
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Black: " + str(black_value))
    ev3.screen.draw_text(0, 50, "Thr : " + str(BLACK_THRESHOLD))
    wait(2000)

# --------------------------------------------------
# Line follower – stay ON BLACK (not edge)
# --------------------------------------------------
def line_follow_black(distance_mm):
    """
    Drive forward while keeping the sensor over the black line.
    - If reflection < BLACK_THRESHOLD → we're on black → go straight.
    - If reflection >= BLACK_THRESHOLD → we're on white → turn left to find black.
    """
    DRIVE_SPEED = 100          # mm/s
    SEEK_TURN_RATE = 40        # deg/s, turn left to search for black

    travelled = 0
    robot.reset()

    while travelled < distance_mm:
        current = color_sensor.reflection()
        if current < BLACK_THRESHOLD:
            # On black – drive straight
            robot.drive(DRIVE_SPEED, 0)
        else:
            # On white – turn left to get back to black
            robot.drive(DRIVE_SPEED, SEEK_TURN_RATE)

        travelled = robot.distance()
        wait(10)

    robot.stop()

# --------------------------------------------------
# Main mission (example: follow line for 50 cm, turn, etc.)
# --------------------------------------------------
def main():
    calibrate_black()

    # Optional arm up
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)

    # Follow the black line for 500 mm (50 cm)
    line_follow_black(500)

    # Celebrate when done
    celebrate()

# --------------------------------------------------
# Run the program
# --------------------------------------------------
if __name__ == "__main__":
    main()
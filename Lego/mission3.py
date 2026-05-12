#!/usr/bin/env pybricks-micropython

"""
Mission 3 – With dynamic colour sensor calibration
===================================================
Calibrates the colour sensor on the real mat before starting,
then follows the black line using the calculated edge threshold.

Uses the lift motor (Port A) as attachment:
  - arm_down() = open/lower to collect/release
  - arm_up()   = close/raise to secure

Path:
 1. Forward 180 mm on line
 2. Left 50°, forward 100 mm
 3. Right 90°, forward 280 mm on line
 4. Right 270°
 5. Lower arm (open), wait, raise arm (close) → secure items
 6. Right 50°, forward 250 mm on line
 7. Right 90°, forward 400 mm on line
 8. Celebrate
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --------------------------------------------------
# Hardware
# --------------------------------------------------
ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)

# Arm motor on Port A
lift_motor = Motor(Port.A)

# Colour sensor – match the port from your sample (S3 in the example)
line_sensor = ColorSensor(Port.S3)

# Robot dimensions (same as sample)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=121)

# Default drive settings – will be overridden by line follower speeds
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Global variables that will be set after calibration
# --------------------------------------------------
TARGET_THRESHOLD = 40   # placeholder – will be updated by calibration
PROPORTIONAL_GAIN = 1.2 # can also be tuned if needed

# --------------------------------------------------
# Calibration function (exactly as in your working sample)
# --------------------------------------------------
def calibrate_sensor():
    """Measure black and white on the mat, compute edge threshold."""
    global TARGET_THRESHOLD

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK")
    ev3.screen.draw_text(0, 50, "Press any btn")

    # Wait for button press
    while len(ev3.buttons.pressed()) == 0:
        wait(10)

    black_value = line_sensor.reflection()
    ev3.speaker.beep(500, 200)

    # Debounce
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

    # Calculate target threshold – exactly the edge of the line
    TARGET_THRESHOLD = (black_value + white_value) / 2

    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))
    wait(2000)   # show calibration results for 2 seconds

# --------------------------------------------------
# Movement helpers
# --------------------------------------------------
def move(distance):
    """Straight move without line following."""
    robot.straight(distance)

def turn(angle):
    """Turn in place (positive = left)."""
    robot.turn(angle)

def celebrate():
    """Sound feedback."""
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()

# --------------------------------------------------
# Arm (attachment) helpers
# --------------------------------------------------
def arm_up():
    """Raise the arm (close attachment)."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)   # up position
    wait(500)

def arm_down():
    """Lower the arm (open attachment)."""
    lift_motor.run_target(100, -110)  # down position
    wait(500)

# --------------------------------------------------
# Line follower – now uses the calibrated TARGET_THRESHOLD
# --------------------------------------------------
def line_follow(distance_mm):
    """
    Follow the black line for **distance_mm** using
    the dynamically calibrated threshold.
    """
    DRIVE_SPEED = 100           # mm/s – slower than default for better control
    travelled = 0

    robot.reset()
    while travelled < distance_mm:
        current_reflection = line_sensor.reflection()
        error = current_reflection - TARGET_THRESHOLD
        steering = error * PROPORTIONAL_GAIN
        robot.drive(DRIVE_SPEED, steering)
        travelled = robot.distance()
        wait(10)                # small pause for stability

    robot.stop()

# --------------------------------------------------
# Main mission
# --------------------------------------------------
def main():
    ev3.screen.clear()

    # 0. Calibrate the colour sensor interactively
    calibrate_sensor()

    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Running Mission 3...")
    wait(500)

    # 1. Forward 180 mm on the line
    line_follow(180)

    # 2. Turn left 50°, then 100 mm on the line (or move(100) if no line)
    turn(50)
    line_follow(100)

    # 3. Turn right 90°, then 280 mm on the line
    turn(-90)
    line_follow(280)

    # 4. Turn right 270°
    turn(-270)

    # 5. Open attachment, wait, close to secure
    arm_down()                 # open / lower
    wait(300)
    arm_up()                   # close / raise
    wait(300)

    # 6. Turn right 50°, then 250 mm on the line
    turn(-50)
    line_follow(250)

    # 7. Turn right 90°, then 400 mm on the line
    turn(-90)
    line_follow(400)

    # 8. Done!
    celebrate()

# --------------------------------------------------
# Run the mission
# --------------------------------------------------
if __name__ == "__main__":
    main()
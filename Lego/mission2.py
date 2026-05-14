#!/usr/bin/env pybricks-micropython

"""
Mission 3 – Corrected line follower with live debug
====================================================
- Calibrates the colour sensor on the real mat.
- Follows the left edge of a black line using proportional control.
- Live EV3 screen shows sensor readings – you can watch the robot react.
- Arm (Port A) used for attachment: down = open, up = close.

Path (same as before):
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
# Hardware setup
# --------------------------------------------------
ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor  = Motor(Port.A)            # Arm attachment

line_sensor = ColorSensor(Port.S3)     # Colour sensor – adjust port if needed

# Robot dimensions (adjust if your robot is different)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=121)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Global calibration values (set during calibration)
# --------------------------------------------------
TARGET_THRESHOLD = 50
PROPORTIONAL_GAIN = 1.8           # increased for a clear reaction
STEERING_SIGN    = 1.0            # change to -1.0 if the robot turns the wrong way

DEBUG = True                      # Set to False to disable screen output

# --------------------------------------------------
# Calibration function
# --------------------------------------------------
def calibrate_sensor():
    global TARGET_THRESHOLD

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK")
    ev3.screen.draw_text(0, 50, "Press any btn")

    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    black_value = line_sensor.reflection()
    ev3.speaker.beep(500, 200)

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

    TARGET_THRESHOLD = (black_value + white_value) / 2

    # Show calibration results
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))
    wait(2000)

    # Safety check: if black and white are almost the same, abort
    if abs(black_value - white_value) < 10:
        ev3.screen.clear()
        ev3.screen.draw_text(0, 20, "Sensor error!")
        ev3.screen.draw_text(0, 40, "Check position / lighting")
        while True:
            ev3.speaker.beep(200, 200)
            wait(2000)

# --------------------------------------------------
# Movement helpers
# --------------------------------------------------
def move(distance):
    robot.straight(distance)

def turn(angle):
    robot.turn(angle)

def celebrate():
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()

# --------------------------------------------------
# Arm helpers
# --------------------------------------------------
def arm_up():
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)    # up / close
    wait(500)

def arm_down():
    lift_motor.run_target(100, -110)   # down / open
    wait(500)

# --------------------------------------------------
# Line follower – corrected and clearly reacting
# --------------------------------------------------
def line_follow(distance_mm):
    """
    Follow the black line for a given distance.
    - Uses the calibrated TARGET_THRESHOLD.
    - Shows live sensor data on the EV3 screen (if DEBUG is True).
    """
    DRIVE_SPEED = 80                     # slightly slower for better control
    travelled = 0
    robot.reset()

    while travelled < distance_mm:
        current = line_sensor.reflection()
        error = current - TARGET_THRESHOLD
        steer = error * PROPORTIONAL_GAIN * STEERING_SIGN

        # ---- LIVE DEBUG ON SCREEN ----
        if DEBUG:
            ev3.screen.clear()
            ev3.screen.draw_text(0,  0, "R:" + str(current))        # reflection
            ev3.screen.draw_text(0, 20, "E:" + str(error))          # error
            ev3.screen.draw_text(0, 40, "S:" + str(steer))          # steering
            ev3.screen.draw_text(0, 60, "D:" + str(travelled))      # distance

        robot.drive(DRIVE_SPEED, steer)
        travelled = robot.distance()
        wait(10)

    robot.stop()
    if DEBUG:
        ev3.screen.clear()

# --------------------------------------------------
# Main mission
# --------------------------------------------------
def main():
    ev3.screen.clear()
    calibrate_sensor()

    # Optional: after calibration, check sensor responsiveness
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Running Mission 3...")
    wait(500)

    # 1. Forward 180 mm on line
    line_follow(180)

    # 2. Turn left 50°, then forward 100 mm (line)
    turn(50)
    line_follow(100)

    # 3. Turn right 90°, then forward 280 mm (line)
    turn(-90)
    line_follow(280)

    # 4. Turn right 270° (big turn)
    turn(-270)

    # 5. Open attachment, wait, close to secure
    arm_down()
    wait(300)
    arm_up()
    wait(300)

    # 6. Turn right 50°, then forward 250 mm (line)
    turn(-50)
    line_follow(250)

    # 7. Turn right 90°, then forward 400 mm (line)
    turn(-90)
    line_follow(400)

    # 8. Celebrate
    celebrate()

if __name__ == "__main__":
    main()
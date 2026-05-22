#!/usr/bin/env pybricks-micropython

"""
Mission 3 – Line Following with Live Proof
===========================================
Shows sensor readings (R/E/S) on the EV3 screen
so you can SEE the robot follow the black line.
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
lift_motor  = Motor(Port.A)          # Arm motor

line_sensor = ColorSensor(Port.S3)   # Colour sensor

robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=121)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Global calibration value
# --------------------------------------------------
TARGET_THRESHOLD = 50

# --------------------------------------------------
# Calibration (exactly like your demo)
# --------------------------------------------------
def calibrate():
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

    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))
    wait(2000)

# --------------------------------------------------
# Line follower with live proof on screen
# --------------------------------------------------
def line_follow(distance_mm):
    DRIVE_SPEED = 100
    PROPORTIONAL_GAIN = 1.2
    STEERING_DIRECTION = -1    # Change to 1 if the robot turns the wrong way

    travelled = 0
    robot.reset()

    while travelled < distance_mm:
        # Read sensor
        current = line_sensor.reflection()
        # Error = how far we are from the edge
        error = current - TARGET_THRESHOLD
        # Steering correction
        steer = error * PROPORTIONAL_GAIN * STEERING_DIRECTION

        # ---- LIVE DEBUG SCREEN (proof that sensor is in control) ----
        ev3.screen.clear()
        ev3.screen.draw_text(0,  0, "R:" + str(current))    # raw reflection
        ev3.screen.draw_text(0, 20, "E:" + str(error))      # error
        ev3.screen.draw_text(0, 40, "S:" + str(steer))      # steering command
        ev3.screen.draw_text(0, 60, "D:" + str(travelled))  # distance so far

        # Apply steering
        robot.drive(DRIVE_SPEED, steer)
        travelled = robot.distance()
        wait(10)

    robot.stop()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Segment done")
    wait(500)

# --------------------------------------------------
# Basic moves
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
    lift_motor.run_target(100, 110)
    wait(500)

<<<<<<< HEAD
    # Follow the black line for 500 mm (50 cm)
    line_follow_black(600)
    # turn(-30)
    # line_follow_black(150)
    # turn(90)
    # line_follow_black(630)
=======
def arm_down():
    lift_motor.run_target(100, -110)
    wait(500)
>>>>>>> fdc32913e5fb14a3bb6d81499236d68c8c1e8a15

# --------------------------------------------------
# Main mission
# --------------------------------------------------
def main():
    calibrate()

    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Mission 3 Running...")
    wait(500)

    # 1. Forward 180 mm on line (watch the screen!)
    line_follow(180)

    # 2. Turn left 50°, then 100 mm on line
    turn(50)
    line_follow(100)

    # 3. Turn right 90°, then 280 mm on line
    turn(-90)
    line_follow(280)

    # 4. Turn right 270° (big turn)
    turn(-270)

    # 5. Arm: open, wait, close
    arm_down()
    wait(300)
    arm_up()
    wait(300)

    # 6. Turn right 50°, then 250 mm on line
    turn(-50)
    line_follow(250)

    # 7. Turn right 90°, then 400 mm on line
    turn(-90)
    line_follow(400)

    # 8. Celebrate
    celebrate()

if __name__ == "__main__":
    main()
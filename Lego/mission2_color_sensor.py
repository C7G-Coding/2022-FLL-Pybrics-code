#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# -----------------------------
# Setup
# -----------------------------

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A)

line_sensor = ColorSensor(Port.S3)

wheel_diameter = 56
axle_track = 123

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# -----------------------------
# Line settings
# -----------------------------

TARGET = 50

DRIVE_SPEED = 105
GAIN = 1.1

# Change this to 1 if the robot turns away from the line.
LINE_SIDE = -1

# If the line turns right and the sensor sees white, this makes it search right.
# If it searches the wrong way, make this negative.
RIGHT_SEARCH_STEER = 75

MAX_STEER = 65

# Measurements from your template
LINE_OUT = 470       # 300 + 170 from your first path
FORWARD_AFTER_LINE = 625
BACK_UP_AMOUNT = 50  # 5 cm


# -----------------------------
# Small helper functions
# -----------------------------

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def pause(time=2000):
    wait(time)


def move(distance):
    robot.straight(distance)


def turn(angle):
    robot.turn(angle)


def celebrate():
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()


# -----------------------------
# Arm
# -----------------------------

def arm_up():
    lift_motor.run_target(100, 110)


def arm_down():
    lift_motor.run_target(100, -5)


# -----------------------------
# Calibration
# -----------------------------

def wait_for_button():
    while len(ev3.buttons.pressed()) == 0:
        wait(10)

    while len(ev3.buttons.pressed()) > 0:
        wait(10)


def calibrate():
    global TARGET

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Sensor on BLACK")
    ev3.screen.draw_text(0, 50, "Press button")
    wait_for_button()

    black_value = line_sensor.reflection()
    ev3.speaker.beep()

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Sensor on WHITE")
    ev3.screen.draw_text(0, 50, "Press button")
    wait_for_button()

    white_value = line_sensor.reflection()
    ev3.speaker.beep()

    TARGET = (black_value + white_value) / 2

    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Black: " + str(black_value))
    ev3.screen.draw_text(0, 35, "White: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Target: " + str(TARGET))
    wait(2000)


# -----------------------------
# Line follow
# -----------------------------

def line_follow(distance_mm, side):
    robot.reset()

    lost_count = 0
    screen_timer = 0

    while abs(robot.distance()) < distance_mm:
        reflection = line_sensor.reflection()

        error = reflection - TARGET
        steer = error * GAIN * side
        steer = clamp(steer, -MAX_STEER, MAX_STEER)

        # If it sees too much white for a little bit, it probably missed
        # the right turn in the black line, so it searches right.
        if reflection > TARGET + 18:
            lost_count = lost_count + 1
        else:
            lost_count = 0

        if lost_count > 5:
            robot.drive(70, RIGHT_SEARCH_STEER)
        else:
            robot.drive(DRIVE_SPEED, steer)

        if screen_timer > 100:
            ev3.screen.clear()
            ev3.screen.draw_text(0, 0, "R: " + str(reflection))
            ev3.screen.draw_text(0, 20, "E: " + str(error))
            ev3.screen.draw_text(0, 40, "S: " + str(steer))
            ev3.screen.draw_text(0, 60, "D: " + str(robot.distance()))
            screen_timer = 0

        wait(10)
        screen_timer = screen_timer + 10

    robot.stop()
    wait(200)


# -----------------------------
# Main
# -----------------------------

def main():
    calibrate()

    lift_motor.reset_angle(0)
    arm_up()

    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Running")
    wait(500)

    # 1. Follow the black line.
    # This should also catch the right turn in the line.
    line_follow(LINE_OUT, LINE_SIDE)

    # 2. After the turn, wait 5 seconds.
    pause(5000)

    # 3. Move forward.
    move(FORWARD_AFTER_LINE)

    # 4. Turn left 90 degrees.
    turn(-90)

    # 5. Lower the arm.
    arm_down()
    wait(300)

    # 6. Move back 5 cm.
    move(-BACK_UP_AMOUNT)

    # 7. Lift the arm.
    arm_up()
    wait(300)

    # -----------------------------
    # Reverse actions to go home
    # -----------------------------

    # Undo the 5 cm backup.
    move(BACK_UP_AMOUNT)

    # Undo the left turn.
    turn(90)

    # Reverse the forward drive.
    move(-FORWARD_AFTER_LINE)

    # Turn around and follow the line back home.
    turn(180)

    # Usually the return side needs to be the opposite of the first side.
    line_follow(LINE_OUT, -LINE_SIDE)

    # Face the same way as the start.
    turn(180)

    celebrate()


if __name__ == "__main__":
    main()
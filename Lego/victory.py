#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

import os

# -----------------------------
# Setup
# -----------------------------

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

wheel_diameter = 56
axle_track = 121

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Fast settings
robot.settings(
    straight_speed=500,
    straight_acceleration=900,
    turn_rate=300,
    turn_acceleration=700
)

SONG_FILE = "janicestfu.wav"
TURN_SPEED = 300


# -----------------------------
# Sound helpers
# -----------------------------

def start_song():
    # Starts the wav file in the background.
    os.system("aplay ./" + SONG_FILE + " >/dev/null 2>&1 & echo $! > /tmp/song_pid.txt")


def stop_song():
    # Stops only the song process that was started.
    try:
        f = open("/tmp/song_pid.txt", "r")
        pid = f.read().strip()
        f.close()

        if pid != "":
            os.system("kill " + pid + " >/dev/null 2>&1")
    except:
        # Backup option if the pid file does not work.
        os.system("killall aplay >/dev/null 2>&1")


# -----------------------------
# Movement
# -----------------------------

def fast_360_with_song():
    robot.reset()

    start_song()
    wait(300)

    # Turn right fast.
    robot.drive(0, TURN_SPEED)

    while abs(robot.angle()) < 360:
        wait(5)

    robot.drive(0, 0)
    wait(100)
    robot.stop()

    stop_song()


# -----------------------------
# Main
# -----------------------------

def main():
    ev3.speaker.beep()

    fast_360_with_song()

    wait(500)
    ev3.speaker.beep(1000, 500)


if __name__ == "__main__":
    main()
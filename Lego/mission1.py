#!/usr/bin/env pybricks-micropython

"""
Mission 1 Forward, Lock, and Return with Heavy Object
========================================================
The robot starts in the launch area.

Steps:
  1. Raise arm to up position.
  2. Wait, then drive straight forward 400 mm (40 cm).
  3. Wait, then lower arm to lock onto the ground/object.
  4. Wait, then drive straight backward 400 mm (40 cm) with increased
     motor force (higher speed/acceleration) to handle the heavy load.
  5. Wait, then beep to signal completion.
"""

# --------------------------------------------------
# Imports (same style as your reference code)
# --------------------------------------------------

# For the lift motor
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

# The lift motor is used in the arm_up / arm_down helpers
lift_motor = Motor(Port.A)

# Import the EV3Brick class – gives access to screen, speaker, etc.
from pybricks.hubs import EV3Brick

# Import the Motor class (already imported above, kept for clarity)
from pybricks.ev3devices import Motor

# Import Port to specify motor connections
from pybricks.parameters import Port

# Import DriveBase – combines two motors into a driving robot
from pybricks.robotics import DriveBase

# Import wait to pause the program between actions
from pybricks.tools import wait


# --------------------------------------------------
# Device setup
# --------------------------------------------------

ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)


# --------------------------------------------------
# Robot measurements
# --------------------------------------------------

# Wheel diameter in mm (used to calculate distance)
wheel_diameter = 56

# Distance between wheel centres in mm (important for accurate turns)
axle_track = 123


# --------------------------------------------------
# DriveBase setup
# --------------------------------------------------

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Default movement settings
robot.settings(straight_speed=200, turn_rate=90)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def move(distance_mm):
    """
    Move the robot straight.
    
    Parameters:
        distance_mm (int): Distance in millimetres.
                           Positive = forward, negative = backward.
    """
    robot.straight(distance_mm)


def arm_up():
    """
    Raise the arm to the UP position.
    Resets the angle to 0, then moves to +110 degrees.
    """
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)


def arm_down():
    """
    Lower the arm to the DOWN position.
    Moves to -110 degrees. the motor holds this position (locked).
    """
    lift_motor.run_target(100, -5)


# --------------------------------------------------
# Main mission routine
# --------------------------------------------------

def main():
    ev3.screen.clear()

    # 1. Arm up, then wait
    arm_up()
    wait(500)

    # 2. Move forward 40 cm, then wait
    move(370)
    wait(300)

    # 3. Arm down (lock onto ground / object), then wait
    arm_down()


    # 4. Move backward 40 cm with more force
    # Temporarily increase speed & acceleration for the heavy load
    # robot.settings(straight_speed=400, straight_acceleration=500)
    move(-370)
    wait(300)
    # Restore the default gentle drive settings
    robot.settings(straight_speed=200, straight_acceleration=200)

    # 5. Final wait, then beep
    wait(500)
    ev3.speaker.beep(1000, 500)   # 1 kHz beep for 500 ms
    ev3.screen.clear()


# --------------------------------------------------
# Run the mission if executed directly
# --------------------------------------------------
if __name__ == "__main__":
    main()
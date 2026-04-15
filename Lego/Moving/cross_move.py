#!/usr/bin/env pybricks-micropython

"""
Cross-shaped movement routine for an EV3 robot using Pybricks.

This program demonstrates how a basic two-wheeled EV3 robot can move in
a path that resembles a cross shape.

The robot will:
1. Move forward from the starting point.
2. Turn right and move to one side.
3. Reverse back to the centre point.
4. Turn and move to the opposite side.
5. Reverse back to the centre point again.
6. Turn and return to the original starting position.
7. Play a short celebration sound.

This example is useful for teaching:
- how to import Pybricks classes and functions,
- how to configure motors and a driving base,
- how to organise repeated behaviour into functions,
- how to control distance-based movement,
- how to control turning,
- how to use pauses between actions.
"""

# Import the EV3Brick class.
# This gives access to the EV3 brick itself, including built-in features
# such as the speaker, buttons, and screen.
from pybricks.hubs import EV3Brick

# Import the Motor class.
# We use this to create motor objects for the left and right wheel motors.
from pybricks.ev3devices import Motor

# Import Port so that we can specify where motors are connected on the EV3.
# For example, Port.B means motor port B on the brick.
from pybricks.parameters import Port

# Import DriveBase.
# This class combines two motors into a simple driving robot and provides
# high-level movement methods such as straight() and turn().
from pybricks.robotics import DriveBase

# Import wait so that we can pause the program for a given number of
# milliseconds between robot actions.
from pybricks.tools import wait


# --------------------------------------------------
# Device setup
# --------------------------------------------------

# Create an EV3Brick object to represent the programmable brick.
ev3 = EV3Brick()

# Create the motor object for the left wheel.
# This motor is connected to output port B.
left_motor = Motor(Port.B)

# Create the motor object for the right wheel.
# This motor is connected to output port C.
right_motor = Motor(Port.C)


# --------------------------------------------------
# Robot measurements
# --------------------------------------------------

# The diameter of the wheels in millimetres.
# This value is used by DriveBase to calculate movement distance.
wheel_diameter = 56

# The distance between the centres of the left and right wheels in
# millimetres. This value is important for accurate turning.
axle_track = 123


# --------------------------------------------------
# DriveBase setup
# --------------------------------------------------

# Create the robot as a DriveBase.
# This allows the two motors to work together as a single driving robot.
robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Set the default movement speed and turn rate for the robot.
#
# straight_speed is measured in millimetres per second.
# turn_rate is measured in degrees per second.
robot.settings(straight_speed=200, turn_rate=90)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def move_and_wait(distance, pause=2000):
    """
    Move the robot in a straight line and then pause.

    Parameters:
        distance (int): The distance to move in millimetres.
                        A positive value moves forward.
                        A negative value moves backward.
        pause (int):    The time to wait after the movement, in milliseconds.

    This function is useful because it groups two common actions:
    1. move the robot,
    2. pause so that the movement can be observed clearly.
    """
    # Move the robot straight for the given distance.
    robot.straight(distance)

    # Pause after the movement.
    wait(pause)


def turn_and_wait(angle, pause=2000):
    """
    Turn the robot and then pause.

    Parameters:
        angle (int): The angle to turn in degrees.
                     A positive angle turns left.
                     A negative angle turns right.
        pause (int): The time to wait after the turn, in milliseconds.

    This function helps reduce repeated code and makes the main routine
    easier to read.
    """
    # Turn the robot by the given angle.
    robot.turn(angle)

    # Pause after the turn.
    wait(pause)


def celebrate():
    """
    Play a short celebration sound at the end of the routine.

    This gives the robot a simple audible signal to show that the
    movement sequence has been completed successfully.
    """
    ev3.speaker.beep()
    wait(300)
    ev3.speaker.beep()


def main():
    """
    Run the main cross-shaped movement routine.

    The robot starts at a centre point, moves forward, then explores one
    side and the opposite side before returning to the original starting
    point.
    """

    # Step 1:
    # Move forward 1000 mm from the starting point.
    move_and_wait(284)

    move_and_wait(-284)

    # # Step 2:
    # # Turn right by 90 degrees.
    # # In Pybricks, a negative angle means a right turn.
    # turn_and_wait(-90)

    # # Move forward 500 mm to the first side of the cross.
    # move_and_wait(500)

    # # Step 3:
    # # Reverse 500 mm back to the turning point.
    # move_and_wait(-500)

    # # Step 4:
    # # Turn 180 degrees so that the robot faces toward the opposite side.
    # move_and_wait(0, 500)  # Optional short pause for clarity.
    # turn_and_wait(180)

    # # Move forward 500 mm to the opposite side of the cross.
    # move_and_wait(500)

    # # Step 5:
    # # Reverse back 500 mm to the centre turning point again.
    # move_and_wait(-500)

    # # Step 6:
    # # Turn 90 degrees so that the robot faces toward the original line.
    # # At this stage, the robot is aligned to return to the start.
    # turn_and_wait(90)

    # # Move forward 1000 mm to return to the original starting position.
    # move_and_wait(1000)

    # Step 7:
    # Play the celebration sound to indicate the routine is complete.
    celebrate()


# This checks whether the file is being run directly.
# If it is, the main() function is executed.
if __name__ == "__main__":
    main()
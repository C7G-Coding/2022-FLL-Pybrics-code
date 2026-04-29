#!/usr/bin/env pybricks-micropython

"""
Custom movement routine for an EV3 robot using Pybricks.

This program demonstrates how a basic two-wheeled EV3 robot can move in
a path and perform actions.

The robot will:
1. Move forward from the starting point.
2. Take a short curve to the left and continue moving in a straight line.
3. Turn right and move a couple of centimeters in a straight line.
4. Turn left.
5. Perform a lower and pull action.
6. Reverse and return to the original starting position.
7. Play a short celebration sound.

"""
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

lift_motor = Motor(Port.A)

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

def move(distance):
    """
    Move the robot in a straight line.

    Parameters:
        distance (int): The distance to move in millimetres.
                        A positive value moves forward.
                        A negative value moves backward.
    """
    # Move the robot straight for the given distance.
    robot.straight(distance)



def turn(angle):
    """
    Turn the robot.

    Parameters:
        angle (int): The angle to turn in degrees.
                     A positive angle turns left.
                     A negative angle turns right.
    """
    # Turn the robot by the given angle.
    robot.turn(angle)


def celebrate():
    """
    Play a short celebration sound at the end of the routine.

    This gives the robot a simple audible signal to show that the
    movement sequence has been completed successfully.
    """
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()


def main():
    """
    Run the main cross-shaped movement routine.

    The robot starts at a centre point, moves forward, then explores one
    side and the opposite side before returning to the original starting
    point.
    """

    # Step 1:
    # Move forward 180 mm(18 cm) from the starting point.
    move(180)

    # Step 2:
    # Turn left 50 degrees.
    # In Pybricks, a negative angle means a right turn.
    turn(50)

    # Move forward 100 mm(10 cm).
    move(100)

    # Step 3:
    # Turn 90 degrees to the right.
    turn(-90)

    # Step 4:
    # Move forward 280 mm(28 cm).
    move(280)


    # Turn 90 degrees to the left.
    turn(90)

    # Step 5:
    #Lower the extension
    lift_motor.run_target(100, -110)
    # Raise the extension
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)

    # Step 6: Reverse and move back to starting position.
    # Reverse
    move(-70)
    # Turn to the left
    turn(90)
    # Move forward 250mm(25 cm) to return to the original starting position.
    move(250)
    # Turn to the left
    turn(90)
    # Move forward for a couple of centimeters
    move(100)
    # Take a short curve to the right
    turn(-50)
    # Move forward
    move(180)


    # Step 7:
    # Play the celebration sound to indicate the routine is complete.
    celebrate()


# This checks whether the file is being run directly.
# If it is, the main() function is executed.
if __name__ == "__main__":
    main()
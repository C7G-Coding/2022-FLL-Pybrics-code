#!/usr/bin/env pybricks-micropython
"""
Demonstrates how to control a standard DriveBase alongside an additional 
medium motor used as a lifting attachment. The script defines modular 
functions for movement and executes a sequential test routine.
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

# EV3Brick is the main interface to the physical EV3 brain (screen, speaker, buttons).
from pybricks.hubs import EV3Brick

# The Motor class handles both the Large motors (used for driving) and the 
# Medium motor (used here for the lift attachment).
from pybricks.ev3devices import Motor

# Port enumeration specifies which physical sockets the motors are plugged into.
from pybricks.parameters import Port

# DriveBase synchronizes two drive motors so we can command the robot to move 
# by distance and angles, rather than individual motor rotations.
from pybricks.robotics import DriveBase

# The wait function pauses the program, allowing physical movements to complete 
# before the next line of code executes.
from pybricks.tools import wait


# =============================================================================
# INITIALISATION
# =============================================================================

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the drive motors. 
# We assume Large motors on Ports B and C for the DriveBase.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the Medium motor on Port A. 
# This will control the lifting mechanism (e.g., a forklift or grabber arm).
lift_motor = Motor(Port.A)   


# =============================================================================
# ROBOT SETUP
# =============================================================================

# Define the physical dimensions of the robot in millimeters.
# wheel_diameter: The diameter of the tires.
# axle_track: The distance between the center point of the two drive wheels.
wheel_diameter = 56
axle_track = 125

# Pass the motors and dimensions into the DriveBase configuration.
robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)


# =============================================================================
# LIFT CALIBRATION & CONSTANTS
# =============================================================================

# Reset the internal rotation sensor of the lift motor to 0 degrees.
# This makes the current physical position the "zero" reference point. 
# It is critical that the lift is in its starting (down) position when the script starts!
lift_motor.reset_angle(0)

# Define target angles for our attachment. 
# Constants are written in UPPERCASE in Python by convention.
LIFT_UP_ANGLE = 90     # The absolute angle representing the "up" position
LIFT_DOWN_ANGLE = 0    # The absolute angle representing the "down" position


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def move(distance):
    """
    Drives the robot straight forward or backward.
    
    distance: The distance to travel in millimeters. 
              Positive values move forward, negative values reverse.
    """
    robot.straight(distance)
    # Pause for 1 second after moving to let momentum settle
    wait(1000)

def turn(angle):
    """
    Turns the robot in place.
    
    angle: The target angle to turn in degrees.
           Positive values turn right (clockwise), negative turn left.
    """
    robot.turn(angle)
    wait(1000)

def lift_up():
    """
    Moves the attachment to the predefined UP position.
    """
    # run_target moves the motor to an absolute angle (90 degrees), 
    # regardless of where it currently is, at a speed of 200 deg/s.
    lift_motor.run_target(200, LIFT_UP_ANGLE)
    wait(500)

def lift_down():
    """
    Moves the attachment to the predefined DOWN position.
    """
    # run_target returns the motor to the absolute 0 degree mark.
    lift_motor.run_target(200, LIFT_DOWN_ANGLE)
    wait(500)


    #Routine

    #Start volume
    ev3.speaker.beep()

    # move forward 
    move(284)

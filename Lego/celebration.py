#!/usr/bin/env pybricks-micropython
"""
Demonstrates basic obstacle avoidance using a Touch Sensor. 
The robot drives forward continuously until it physically bumps into an object, 
at which point it stops, plays a sound, reverses, turns around, and continues.
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# =============================================================================
# INITIALISATION
# =============================================================================

# Initialize the EV3 brain interface
ev3 = EV3Brick()

# Initialize the drive motors on Ports B and C
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the Touch Sensor on Port 1. 
# The Touch Sensor is a simple digital switch that returns True when pressed.
touch = TouchSensor(Port.S1)

# Configure the DriveBase (wheel diameter 56mm, axle track 125mm)
robot = DriveBase(left_motor, right_motor, 56, 125)


# =============================================================================
# MAIN EVENT LOOP
# =============================================================================
    
    # Command the robot to drive forward indefinitely at 200 mm/s with 0 steering.
    # Because this is inside a while loop, it keeps refreshing the command.
    robot.drive(200, 0)


        # ---------------------------------
        # EXCEPTION HANDLING
        # ---------------------------------
        # Attempt to play a specific audio file. If the file "oopsy.wav" is missing 
        # from the EV3's file system, the program would normally crash. 
        # The try/except block catches this FileNotFoundError and safely defaults 
        # to a standard beep, keeping the robot operational.
        try:
             ev3.speaker.play_file("")
        except:
            ev3.speaker.beep()

        # Wait 1.5 seconds (1500 ms) to let the sound finish playing
        wait(1500)

        # ---------------------------------
        # EVASIVE MANEUVER
        # ---------------------------------
        # Move backwards by 100 millimeters to clear the obstacle
        robot.straight(-100)

        # Turn 180 degrees to face the opposite direction
        robot.turn(180)

        # Brief pause to allow momentum to settle after turning
        wait(500)

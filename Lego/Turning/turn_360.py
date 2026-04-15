#!/usr/bin/env pybricks-micropython
"""
Demonstrates multiple 360-degree point turns in alternating directions.
This routine helps verify that the physical wheel diameter and axle track 
measurements are perfectly calibrated for both left and right pivots.
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# =============================================================================
# INITIALISATION
# =============================================================================

# Initialize the EV3 brain interface
ev3 = EV3Brick()

# Initialize the left and right drive motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Kinematic setup - critical for accurate turns
wheel_diameter = 56      
axle_track = 121      

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)


# =============================================================================
# MAIN PROGRAM EXECUTION
# =============================================================================

# Signal the start of the routine
ev3.speaker.beep()

# Set how many times we want the back-and-forth sequence to repeat
sequence_count = 3

for i in range(sequence_count):
    # Print the current step to the console so students can track execution
    print("Sequence " + str(i + 1) + ": Turning 360 degrees Right (Clockwise)")
    
    # A positive angle turns the robot to the right
    robot.turn(360)
    
    # CRITICAL: Pause for 1 second. 
    # If we immediately reverse direction, the physical momentum of the robot 
    # will fight the motors, causing wheel slip and ruining the accuracy of the turn.
    wait(1000)

    print("Sequence " + str(i + 1) + ": Turning 360 degrees Left (Counter-Clockwise)")
    
    # A negative angle turns the robot to the left
    robot.turn(-360)
    
    # Pause again before the loop restarts
    wait(1000)

# Play a higher-pitched beep to signal completion
ev3.speaker.beep(frequency=1000, duration=500)
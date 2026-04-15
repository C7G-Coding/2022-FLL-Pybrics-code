#!/usr/bin/env pybricks-micropython
"""
Demonstrates how to use a Gyro Sensor to maintain a straight heading on an EV3 robot.
This script uses a basic Proportional (P) control loop to dynamically adjust the 
steering based on the current deviation from the target angle.
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

# EV3Brick represents the EV3 programmable brick (the "brain"). 
# Required to interact with the onboard screen, speaker, and buttons.
from pybricks.hubs import EV3Brick

# Motor and GyroSensor classes provide the software interface to the physical hardware.
from pybricks.ev3devices import Motor, GyroSensor

# The Port enumeration defines the physical ports on the EV3 brick. 
# Used to specify where sensors (1-4) and motors (A-D) are plugged in.
from pybricks.parameters import Port

# DriveBase is a helper class that pairs two independent motors into a single 
# drivable entity. It handles the underlying math required to convert desired 
# speed and steering into individual motor rotations.
from pybricks.robotics import DriveBase

# The wait function pauses the program's execution for a specified number of milliseconds.
# Crucial in hardware programming to give mechanical parts or sensors time to settle.
from pybricks.tools import wait


# =============================================================================
# INITIALISATION
# =============================================================================

# Create an instance of the EV3 brick to access the speaker and screen
ev3 = EV3Brick()

# Initialise the left and right motors on ports B and C respectively.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialise the Gyro sensor on port 4.
gyro = GyroSensor(Port.S4)

# Configure the DriveBase. 
# Parameters: left_motor, right_motor, wheel_diameter (mm), axle_track (mm)
# The axle_track is the distance between the two wheels.
robot = DriveBase(left_motor, right_motor, 56, 125)


# =============================================================================
# SENSOR CALIBRATION
# =============================================================================

# Reset the gyro sensor's current heading to 0 degrees.
# This establishes our "target straight" direction.
gyro.reset_angle(0)

# Pause for 500ms (half a second) to ensure the gyro hardware has fully reset 
# before the robot attempts to read from it or start moving.
wait(500)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def drive_straight(speed=200, duration=5000, correction_gain=2):
    """
    Drives the robot in a straight line for a specified duration using 
    proportional feedback from the gyro sensor to correct its heading.
    
    Parameters:
    -----------
    speed : int
        The forward driving speed in millimeters per second (default: 200).
    duration : int
        The total time to drive straight, in milliseconds (default: 5000).
    correction_gain : int or float
        The proportional multiplier (P-gain). Determines how aggressively the 
        robot steers back to 0 degrees when it drifts off course (default: 2).
    """
    
    # Initialize our loop counter to track how long we have been driving
    start_time = 0

    # Continue looping until our elapsed time reaches the requested duration
    while start_time < duration:
        
        # Read the current angle from the gyro. 
        # A positive value means the robot has drifted right; negative means left.
        angle = gyro.angle()

        # Calculate the required steering correction.
        # We multiply the current drift angle by our gain, and invert the sign (-).
        # Inverting the sign is crucial: if we drift +5 degrees (right), we need a 
        # -10 steering value to steer left and bring the angle back to 0.
        correction = -angle * correction_gain

        # Command the robot to drive forward at the target speed, applying the 
        # calculated steering correction.
        robot.drive(speed, correction)

        # Update the EV3 screen with the current angle for real-time debugging
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Angle: " + str(angle))

        # Pause briefly to prevent the loop from running too fast and overwhelming 
        # the EV3's processor, then increment our tracked time by the same amount.
        wait(10)
        start_time += 10

    # Once the loop completes (duration reached), halt the motors.
    robot.stop()


# =============================================================================
# MAIN PROGRAM EXECUTION
# =============================================================================

# Emit a beep to signal to the user that the program is starting
ev3.speaker.beep()

# Call the drive_straight function using keyword arguments for clarity
# This will drive the robot at 200 mm/s for 5000 ms (5 seconds)
drive_straight(speed=200, duration=5000)

# Emit a final beep to signal that the movement has successfully completed
ev3.speaker.beep()
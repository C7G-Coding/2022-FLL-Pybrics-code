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

# Start an infinite loop to continuously monitor the sensor and update behavior.
# This is a standard architecture in robotics known as "polling".
while True:
    
    # Command the robot to drive forward indefinitely at 200 mm/s with 0 steering.
    # Because this is inside a while loop, it keeps refreshing the command.
    robot.drive(200, 0)

    # Poll the touch sensor. The .pressed() method returns a boolean (True/False).
    if touch.pressed():
        
        # Immediate reaction: Stop the motors to prevent pushing into the obstacle.
        robot.stop()

        # Output to the console for debugging purposes.
        print("Touch pressed! Obstacle detected.")

        # ---------------------------------
        # EXCEPTION HANDLING
        # ---------------------------------
        # Attempt to play a specific audio file. If the file "oopsy.wav" is missing 
        # from the EV3's file system, the program would normally crash. 
        # The try/except block catches this FileNotFoundError and safely defaults 
        # to a standard beep, keeping the robot operational.
        try:
             ev3.speaker.play_file("oopsy.wav")
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

        # ---------------------------------
        # STATE MANAGEMENT (DEBOUNCING)
        # ---------------------------------
        # 🔥 CRITICAL: If the robot backed up but the sensor is somehow STILL pressed 
        # (e.g., it got snagged, or a user is holding it), the loop would immediately 
        # trigger again. This nested while loop acts as a block, pausing the main 
        # program flow until the physical button is explicitly released.
        while touch.pressed():
            wait(10) # Check every 10ms, do nothing until False.
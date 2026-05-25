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
robot.drive(600, 0)
try:
  ev3.speaker.play_file("janicestfu.wav")
except:
    ev3.speaker.beep()

 # Wait 1.5 seconds (1500 ms) to let the sound finish playing
wait(1500)

robot.turn(720)
robot.drive(-600,0)



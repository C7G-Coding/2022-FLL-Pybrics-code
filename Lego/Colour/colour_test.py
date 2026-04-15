#!/usr/bin/env pybricks-micropython
"""
Demonstrates interactive Color Sensor calibration and implements a basic 
Proportional (P) control loop to follow the edge of a line.
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# The ColorSensor outputs a reflection value between 0 (dark) and 100 (light).
line_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, 56, 121)

# =============================================================================
# CALIBRATION LOGIC
# =============================================================================
# Environmental lighting changes constantly. We cannot hardcode a value like "50" 
# to mean "the edge of the line" because 50 might be pure white in a dark room, 
# or pure black near a sunny window. We must calibrate dynamically.

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on BLACK")
ev3.screen.draw_text(0, 50, "Press any btn")

# 1. Wait for user to place the robot and press a button
# ev3.buttons.pressed() returns a collection of pressed buttons. 
# We loop and do nothing (wait) as long as no buttons are being pressed.
while len(ev3.buttons.pressed()) == 0:
    wait(10)
    
# Take the reading (e.g., might return 12)
black_value = line_sensor.reflection()

ev3.speaker.beep(500, 200)

# Debounce: Wait for the user to let go of the button before moving to step 2
while len(ev3.buttons.pressed()) > 0:
    wait(10)

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")

# 2. Wait for user to place the robot on white and press a button
while len(ev3.buttons.pressed()) == 0:
    wait(10)
    
# Take the reading (e.g., might return 88)
white_value = line_sensor.reflection()

ev3.speaker.beep(1000, 200)

# Debounce again
while len(ev3.buttons.pressed()) > 0:
    wait(10)

# 3. Calculate the Target Threshold
# We want to follow the *edge* of the line, meaning the sensor should be 
# hovering exactly halfway between the black line and the white floor.
TARGET_THRESHOLD = (black_value + white_value) / 2

# Display results
ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))

print("Calibration Complete. Threshold:", TARGET_THRESHOLD)
wait(3000) 


# =============================================================================
# PROPORTIONAL (P) CONTROL LOOP
# =============================================================================

# DRIVE_SPEED is constant. The robot always moves forward at 100 mm/s.
DRIVE_SPEED = 100       

# PROPORTIONAL_GAIN dictates how aggressively the robot turns to fix an error.
# If the robot "wobbles" too violently, lower this number. 
# If it is too sluggish and loses the line on a curve, raise this number.
PROPORTIONAL_GAIN = 1.2 

ev3.speaker.beep()
ev3.screen.clear()
ev3.screen.draw_text(0, 50, "Following Line...")

while True:
    
    # Step A: Where are we right now?
    current_reflection = line_sensor.reflection()
    
    # Step B: How far off track are we? (Calculate the Error)
    # If Threshold is 50, and we read 50: Error is 0 (Perfect!)
    # If we read 80 (too white): Error is 30 (Positive)
    # If we read 20 (too black): Error is -30 (Negative)
    error = current_reflection - TARGET_THRESHOLD
    
    # Step C: How hard should we steer to fix it?
    # We multiply the error by our gain. 
    # A positive steering value turns the DriveBase right.
    # A negative steering value turns the DriveBase left.
    # (Note: If following the opposite edge of the line, you must multiply by -1)
    steering = error * PROPORTIONAL_GAIN
    
    # Step D: Apply the steering correction while driving forward
    robot.drive(DRIVE_SPEED, steering)
    
    wait(10)
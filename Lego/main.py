#!/usr/bin/env pybricks-micropython

"""
Main mission control for LEGO League robot
Combine and reuse functions from your other files here
"""

# =============================================================================
# IMPORTS - Bring in everything you need
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# =============================================================================
# INITIALIZE ALL YOUR HARDWARE
# =============================================================================

ev3 = EV3Brick()

# Drive motors (adjust ports if different)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Attachment motors (adjust ports as needed)
lift_motor = Motor(Port.A)  # from raise.py, lower.py

# Sensors (adjust ports based on your robot)
color_sensor = ColorSensor(Port.S3)  # from colour_test.py
gyro_sensor = GyroSensor(Port.S4)    # from drive_correction.py
touch_sensor = TouchSensor(Port.S1)  # from touch_sensor.py
ultrasonic = UltrasonicSensor(Port.S2)  # from ultra_sound_test.py

# Robot setup
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=125)

# =============================================================================
# CALIBRATION FUNCTIONS (from your existing files)
# =============================================================================

def calibrate_line_follower():
    """
    Calibrate black and white values for line following
    Adapted from colour_test.py
    """
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK")
    ev3.screen.draw_text(0, 50, "Press any btn")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    black_value = color_sensor.reflection()
    ev3.speaker.beep(500, 200)
    
    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on WHITE")
    ev3.screen.draw_text(0, 50, "Press any btn")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    white_value = color_sensor.reflection()
    ev3.speaker.beep(1000, 200)
    
    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    
    threshold = (black_value + white_value) / 2
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(threshold))
    
    wait(3000)
    return threshold

def reset_gyro():
    """Reset gyro sensor for straight driving (from drive_correction.py)"""
    gyro_sensor.reset_angle(0)
    wait(500)

# =============================================================================
# MOVEMENT FUNCTIONS (combine what you learned)
# =============================================================================

def drive_straight(distance_mm, speed=200):
    """Drive a specific distance in a straight line"""
    robot.straight(distance_mm)
    wait(500)

def turn_degrees(angle, speed=90):
    """Turn robot by specified angle (positive = right, negative = left)"""
    robot.settings(turn_rate=speed)
    robot.turn(angle)
    robot.settings(turn_rate=90)  # reset to default
    wait(500)

def drive_with_gyro(distance_mm, speed=200, gain=2):
    """
    Drive straight using gyro correction for accuracy
    Adapted from drive_correction.py
    """
    reset_gyro()
    start_time = 0
    duration = abs(distance_mm / speed) * 1000  # convert to milliseconds
    
    if distance_mm > 0:
        while start_time < duration:
            angle = gyro_sensor.angle()
            correction = -angle * gain
            robot.drive(speed, correction)
            wait(10)
            start_time += 10
    else:
        # Driving backwards
        while start_time < duration:
            angle = gyro_sensor.angle()
            correction = -angle * gain
            robot.drive(speed, correction)
            wait(10)
            start_time += 10
    
    robot.stop()
    wait(500)

def follow_line(distance_mm, threshold, speed=100, gain=1.2):
    """
    Follow a line edge for a specific distance
    Adapted from colour_test.py
    """
    # Calculate how long to run based on speed
    duration = abs(distance_mm / speed) * 1000
    start_time = 0
    
    while start_time < duration:
        reflection = color_sensor.reflection()
        error = reflection - threshold
        steering = error * gain
        robot.drive(speed, steering)
        wait(10)
        start_time += 10
    
    robot.stop()
    wait(500)

# =============================================================================
# ATTACHMENT FUNCTIONS (from raise.py, lower.py, medium_motor.py)
# =============================================================================

def lift_up():
    """Raise the lifting mechanism"""
    lift_motor.run_target(200, 90)
    wait(500)

def lift_down():
    """Lower the lifting mechanism"""
    lift_motor.run_target(200, 0)
    wait(500)

def lift_to_angle(angle, speed=100):
    """Move lift to specific angle"""
    lift_motor.run_target(speed, angle)
    wait(500)

# =============================================================================
# MISSION FUNCTIONS - WRITE YOUR OWN HERE!
# =============================================================================
    # Replace your MISSION FUNCTIONS section with this test:

def mission_1():
    """Test mission - just move and beep"""
    print("Starting test mission")
    ev3.speaker.beep()
    drive_straight(200)  # Move forward 20cm
    turn_degrees(90)     # Turn right
    drive_straight(200)  # Move another 20cm
    ev3.speaker.beep(1000, 500)
    print("Test complete")

def main():
    ev3.speaker.beep()
    ev3.screen.draw_text(0, 50, "Press center button")
    
    # Wait for button press
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    mission_1()

if __name__ == "__main__":
    main()
    
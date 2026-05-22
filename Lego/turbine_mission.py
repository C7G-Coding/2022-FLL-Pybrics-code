#!/usr/bin/env pybricks-micropython

"""
Turbine and Car Mission
=========================
1. Move straight 70 cm
2. Turn right 20 degrees
3. Do the following 4 times:
      - Move forward 10 cm
      - Move backward 5 cm
4. Wait 5 seconds
5. Move backward 10 cm
6. Turn left 90 degrees
7. Move forward 20 cm
8. Raise arm high
9. Wait 5 seconds
10. Move backward 50 cm
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --------------------------------------------------
# Hardware setup
# --------------------------------------------------
ev3 = EV3Brick()

# Initialize the drive motors on Ports B and C
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the Touch Sensor on Port 1. 
# The Touch Sensor is a simple digital switch that returns True when pressed.
touch = TouchSensor(Port.S1)

# Configure the DriveBase (wheel diameter 56mm, axle track 125mm)
robot = DriveBase(left_motor, right_motor, 56, 125)
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
right_motor = Motor(Port.C)   # Arm control

# Robot measurements (adjust if needed)
wheel_diameter = 56
axle_track = 123               # You can use 121 if that's your exact robot

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def move(distance_mm):
    """Move straight: positive = forward, negative = backward."""
    robot.straight(distance_mm)

def turn(angle):
    """Turn in place: positive = left, negative = right."""
    robot.turn(angle)

def arm_up():
    """Raise the arm to its high position."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)   # Up angle (adjust if needed)
    wait(500)

def arm_down():
    """Lower the arm (not used here, but available)."""
    lift_motor.run_target(100, -5)
    wait(500)

# --------------------------------------------------
# Main mission function
# --------------------------------------------------
def turbine_and_car_mission():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Turbine & Car")

    # 1. Move straight 70 cm (700 mm)
    move(650)

    # 2. Turn right 20 degrees
    turn(46)

    # 3. Do the next two steps 4 times:
    for _ in range(4):
        move(100)   # forward 10 cm
        move(-50)   # backward 5 cm

    # 4. Wait for 5 seconds
    wait(2000)

    # 5. Move backward 10 cm
    turn(-46)

    # 6. Turn left 90 degrees
   
    move(-600)

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

        # # Turn 180 degrees to face the opposite direction
        # robot.turn(180)

        # # Brief pause to allow momentum to settle after turning
        # wait(500)

        # # ---------------------------------
        # # STATE MANAGEMENT (DEBOUNCING)
        # # ---------------------------------
        # # 🔥 CRITICAL: If the robot backed up but the sensor is somehow STILL pressed 
        # # (e.g., it got snagged, or a user is holding it), the loop would immediately 
        # # trigger again. This nested while loop acts as a block, pausing the main 
        # # program flow until the physical button is explicitly released.
        # while touch.pressed():
        #     wait(10) # Check every 10ms, do nothing until False.
    # Optional: sound to mark completion
    ev3.speaker.beep(1000, 300)
    ev3.screen.clear()

# --------------------------------------------------
# Run the mission when the file is executed
# --------------------------------------------------
if __name__ == "__main__":
    turbine_and_car_mission()
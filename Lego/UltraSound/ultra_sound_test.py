#!/usr/bin/env pybricks-micropython

"""
Ultrasonic Sensor Demonstration for EV3 with Pybricks

This program demonstrates a simple use of the ultrasonic sensor on an
EV3 robot. The robot drives forward until it detects an object within
a specified distance. It then stops, beeps, waits for a moment, and
reverses a short distance.

This example is suitable for beginner robotics students because it
demonstrates:
- importing modules,
- creating hardware objects,
- reading a sensor,
- using constants,
- using a loop,
- making decisions with an if statement,
- controlling a robot with a DriveBase.
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase


from pybricks.tools import wait
ev3 = EV3Brick()

# Create the motor object for the left wheel.
# The motor is connected to Port B on the EV3.
left_motor = Motor(Port.B)

# Create the motor object for the right wheel.
# The motor is connected to Port C on the EV3.
right_motor = Motor(Port.C)

# Create a DriveBase object.
# A DriveBase combines the two drive motors into a robot that can move
# forward, backward, and turn.
#
# wheel_diameter is the diameter of the wheels in millimetres.
# axle_track is the distance between the centres of the two wheels.
#
# These measurements are important because they affect the accuracy of
# the robot's movement.
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=118)

# Create the ultrasonic sensor object.
# This tells the program that an ultrasonic sensor is connected to
# sensor Port S4.
ultrasonic = UltrasonicSensor(Port.S2)


# ---------------------------
# Constants / configuration
# ---------------------------

# SAFE_DISTANCE is the distance at which the robot must stop.
# The ultrasonic sensor returns distance in millimetres.
# 200 mm = 20 cm.
SAFE_DISTANCE = 150

# DRIVE_SPEED is the forward speed of the robot in millimetres per second.
DRIVE_SPEED = 120

# REVERSE_DISTANCE is how far the robot must move backward after it
# detects an object.
REVERSE_DISTANCE = 100

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor  = Motor(Port.A)   # Arm control

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
    wait(520)

def main():
    """
    Run the main ultrasonic sensor demonstration.

    The robot moves forward while repeatedly checking the distance to
    the nearest object in front of it.

    If no object is close enough, the robot keeps moving forward.

    If an object is detected within the safe distance:
    1. the robot stops,
    2. the EV3 beeps,
    3. the program waits briefly,
    4. the robot reverses,
    5. the EV3 beeps again,
    6. the program ends.
    """

    # Make a beep sound at the start of the program so that the user
    # knows the robot is about to begin.
    ev3.speaker.beep()

    # Print an introductory message to the console.
    # This is useful when the program is run from VS Code because it
    # helps the user understand what the program is doing.
    print("Ultrasonic sensor demo starting...")
    print("Robot will drive forward until an object is closer than 200 mm.")
    move(470)
    wait(200)
    turn(-46)
    move(430)
    arm_up()
    
    wait(200)

    move(-200)

    turn(90)
    move(100)
    turn(90)
    robot.drive(100,0)
    

    # Start an infinite loop.
    # The robot will keep checking the distance until we explicitly
    # break out of the loop.
    while True:

        # Read the current distance measured by the ultrasonic sensor.
        # The value returned is in millimetres.
        distance = ultrasonic.distance()

        # Print the measured distance so that the user can observe the
        # sensor readings while the program runs.
        print("Distance:", distance, "mm")

        # Check whether the detected object is within the safe distance.
        if distance <= SAFE_DISTANCE:
            # Play a beep sound to indicate that an object has been detected.
            ev3.speaker.beep()
            arm_down()
             # Print a message to the console for clarity.
            print("Object detected. Let's gooo.")
            turn(20)
            move(300)

            break

    # Print a final completion message.
    print("Demo complete.")


# This condition checks whether this file is being run directly.
# If it is, the main() function is called.
# This is a common Python best practice because it keeps the program
# organised and makes the code easier to reuse later.
if __name__ == "__main__":
    main()
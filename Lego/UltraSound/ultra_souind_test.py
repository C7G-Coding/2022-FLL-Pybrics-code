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

# Import the EV3Brick class.
# This gives us access to the EV3 brick itself, including features such
# as the speaker, buttons, and screen.
from pybricks.hubs import EV3Brick

# Import the Motor class so that we can create motor objects for the
# left and right wheels of the robot.
# Import the UltrasonicSensor class so that we can create an object
# representing the ultrasonic sensor connected to the EV3.
from pybricks.ev3devices import Motor, UltrasonicSensor

# Import Port so that we can refer to the physical ports on the EV3
# brick, such as motor ports B and C, and sensor port S4.
from pybricks.parameters import Port

# Import DriveBase, which makes it easier to control a two-wheel robot.
# Instead of controlling each motor separately all the time, we can use
# higher-level movement commands such as drive(), straight(), and turn().
from pybricks.robotics import DriveBase

# Import wait so that we can pause the program for a specified number
# of milliseconds. This is useful when we want the robot to stop briefly
# before continuing with the next action.
from pybricks.tools import wait


# Create an EV3Brick object.
# This represents the EV3 brick and allows us to use built-in features
# such as the speaker for beeps.
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
ultrasonic = UltrasonicSensor(Port.S4)


# ---------------------------
# Constants / configuration
# ---------------------------

# SAFE_DISTANCE is the distance at which the robot must stop.
# The ultrasonic sensor returns distance in millimetres.
# 200 mm = 20 cm.
SAFE_DISTANCE = 200

# DRIVE_SPEED is the forward speed of the robot in millimetres per second.
DRIVE_SPEED = 120

# REVERSE_DISTANCE is how far the robot must move backward after it
# detects an object.
REVERSE_DISTANCE = 100


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

            # Stop the robot immediately because an object is too close.
            robot.stop()

            # Play a beep sound to indicate that an object has been detected.
            ev3.speaker.beep()

            # Print a message to the console for clarity.
            print("Object detected. Stopping.")

            # Wait for 1 second before reversing.
            # 1000 milliseconds = 1 second.
            wait(1000)

            # Move the robot backward by the specified reverse distance.
            # A negative value means backward movement.
            robot.straight(-REVERSE_DISTANCE)

            # Play another beep to indicate that the reverse action is complete.
            ev3.speaker.beep()

            # Print a final message.
            print("Reversed away from object.")

            # Break out of the loop so that the program can end.
            break

        # If no object is within the safe distance, keep driving forward.
        # The first argument is forward speed in mm/s.
        # The second argument is turn rate. A value of 0 means drive straight.
        robot.drive(DRIVE_SPEED, 0)

        # Pause briefly before taking the next sensor reading.
        # This small delay makes the loop easier to manage and prevents
        # it from running unnecessarily fast.
        wait(100)

    # Stop the robot at the end of the program to ensure it is no longer moving.
    robot.stop()

    # Print a final completion message.
    print("Demo complete.")


# This condition checks whether this file is being run directly.
# If it is, the main() function is called.
# This is a common Python best practice because it keeps the program
# organised and makes the code easier to reuse later.
if __name__ == "__main__":
    main()
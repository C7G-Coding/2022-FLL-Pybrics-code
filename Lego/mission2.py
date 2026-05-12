#!/usr/bin/env pybricks-micropython
# arm must start down
"""
Custom movement routine with line following
============================================
Now uses a color sensor to stay on a black line while driving
straight forward and on the return journey.
"""

from pybricks.ev3devices import Motor
from pybricks.parameters import Port

lift_motor = Motor(Port.A)

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  NEW – import the colour sensor
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pybricks.ev3devices import ColorSensor

# --------------------------------------------------
# Device setup (updated with colour sensor)
# --------------------------------------------------

ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  NEW – colour sensor on port S1 (change if yours is on S2, S3 …)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
color_sensor = ColorSensor(Port.S1)

# Robot measurements
wheel_diameter = 56
axle_track = 123

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions (original ones kept, plus a NEW line follower)
# --------------------------------------------------

def move(distance):
    """Simple straight move – no line following."""
    robot.straight(distance)

def turn(angle):
    robot.turn(angle)

def celebrate():
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()
    ev3.speaker.beep()
    wait(100)
    ev3.speaker.beep()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  NEW – line following function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def line_follow(distance_mm):
    """
    Drive forward for **distance_mm** while keeping the robot
    centered on a black line.

    - The sensor should be mounted between the wheels, pointing down.
    - Black gives a low reflection (e.g. <20), white gives a high value (e.g. >60).
    - Adjust THRESHOLD and PROPORTIONAL_GAIN to match your mat and lighting.
    """

    # Threshold between black and white (calibrate for your environment)
    THRESHOLD = 40          # reflection value: <40 = black, >40 = white
    PROPORTIONAL_GAIN = 1.2 # how strongly to steer (tune this!)

    base_speed = 150                # mm/s – forward speed while line following
    distance_travelled = 0          # keep track for stopping

    # Reset the drivebase distance counter
    robot.reset()

    while distance_travelled < distance_mm:
        # Read reflected light intensity (0–100)
        reflection = color_sensor.reflection()

        # Calculate error: how far from the threshold we are
        error = reflection - THRESHOLD

        # Turn rate = proportional gain * error
        # (negative error → turn left to find black, positive → turn right)
        steer = PROPORTIONAL_GAIN * error

        # Drive with forward speed and calculated steer
        robot.drive(base_speed, steer)

        # Update how far we've gone (in mm)
        distance_travelled = robot.distance()

        # Small pause so the loop doesn't run too fast (10 ms is fine)
        wait(10)

    # Stop smoothly
    robot.stop()


# --------------------------------------------------
# Main routine – now uses line_follow()
# --------------------------------------------------

def main():
    ev3.screen.clear()

    # Step 1: Move forward 180 mm WHILE FOLLOWING THE BLACK LINE
    line_follow(180)

    # Step 2: Turn left 50° (no line, so use normal turn)
    # turn(50)
    turn(30)

    # Move forward 100 mm – still on a line? If yes, use line_follow(100)
    # move(100)                
    line_follow(120)

    # Step 3: Turn right 90°
    turn(-90)

    # Step 4: Move forward 280 mm – if on a line, use 
    line_follow(280)
    # move(280)                 

    # Turn left 90°
    turn(90)

    #Get closer to mission2
    move(30)

    # Step 5: Lower arm
    lift_motor.run_target(100, -110)

    # Step 6: Reverse
    move(-30)
    wait(500)

    #Raise arm
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)


    # Return (now also using line following)
    # Reverse 70 mm (no line, so move works)
    move(-70)

    turn(90)

    # Move forward 250 mm BACK along the line – use 
    line_follow(280)

    turn(90)

    # move(100)                   
    line_follow(100)

    turn(-50)

    # Final approach 180 mm on the line
    line_follow(180)

    # Play the celebration sound to indicate the routine is complete
    celebrate()

if __name__ == "__main__":
    main()
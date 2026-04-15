# Import the EV3Brick class.
# This gives access to the EV3 brick itself, including built-in features
# such as the speaker, buttons, and screen.
from pybricks.hubs import EV3Brick

# Import the Motor class.
# We use this to create motor objects for the left and right wheel motors.
from pybricks.ev3devices import Motor

# Import Port so that we can specify where motors are connected on the EV3.
# For example, Port.B means motor port B on the brick.
from pybricks.parameters import Port

# Import DriveBase.
# This class combines two motors into a simple driving robot and provides
# high-level movement methods such as straight() and turn().
from pybricks.robotics import DriveBase

# Import wait so that we can pause the program for a given number of
# milliseconds between robot actions.
from pybricks.tools import wait


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
right_motor = Motor(Port.C)


# --------------------------------------------------
# Robot measurements
# --------------------------------------------------

# The diameter of the wheels in millimetres.
# This value is used by DriveBase to calculate movement distance.
wheel_diameter = 56

# The distance between the centres of the left and right wheels in
# millimetres. This value is important for accurate turning.
axle_track = 123


# --------------------------------------------------
# DriveBase setup
# --------------------------------------------------

# Create the robot as a DriveBase.
# This allows the two motors to work together as a single driving robot.
robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Set the default movement speed and turn rate for the robot.
#
# straight_speed is measured in millimetres per second.
# turn_rate is measured in degrees per second.
robot.settings(straight_speed=300, turn_rate=90)


def move_and_wait(distance, pause=2000):
    """
    Move the robot in a straight line and then pause.

    Parameters:
        distance (int): The distance to move in millimetres.
                        A positive value moves forward.
                        A negative value moves backward.
        pause (int):    The time to wait after the movement, in milliseconds.

    This function is useful because it groups two common actions:
    1. move the robot,
    2. pause so that the movement can be observed clearly.
    """
    # Move the robot straight for the given distance.
    robot.straight(distance)

    # Pause after the movement.
    wait(pause)

def celebrate():
    """
    Play a short celebration sound at the end of the routine.

    This gives the robot a simple audible signal to show that the
    movement sequence has been completed successfully.
    """
    ev3.speaker.beep()
    wait(300)
    ev3.speaker.beep()

def main():
    """
    Run the main cross-shaped movement routine.

    The robot starts at a centre point, moves forward to one arm of the
    cross, returns to centre, then repeats for the opposite arm and both
    side arms before celebrating.
    """

    # Step 1: Move forward (north arm)
    move_and_wait(284)

    # Step 2: Return to centre
    move_and_wait(-284)

    # # Step 3: Turn right 90° to face south arm direction,
    # #         then move forward (south arm)
    # robot.turn(180)
    # wait(500)
    # move_and_wait(284)

    # # Step 4: Return to centre
    # move_and_wait(-284)

    # # Step 5: Turn to face the right arm (east)
    # robot.turn(-90)
    # wait(500)
    # move_and_wait(284)

    # # Step 6: Return to centre
    # move_and_wait(-284)

    # # Step 7: Turn to face the left arm (west)
    # robot.turn(180)
    # wait(500)
    # move_and_wait(284)

    # # Step 8: Return to centre and face original direction
    # move_and_wait(-284)
    # robot.turn(-90)
    # wait(500)

    # Step 9: Celebrate!
    celebrate()
# This checks whether the file is being run directly.
# If it is, the main() function is executed.
if __name__ == "__main__":
    main()

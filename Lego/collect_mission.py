#!/usr/bin/env pybricks-micropython

"""
Turbine and Car Mission – Gyro‑Accurate Turning + Ultrasonic Touch
===================================================================
1. Move forward 10 cm
2. Turn left 50° (gyro‑controlled)
3. Move forward until VERY close to object (≤ 30 mm) using ultrasonic
4. Lower the arm
5. Wait 1 second
6. Raise the arm
7. Move backward 20 cm
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --------------------------------------------------
# Hardware setup
# --------------------------------------------------
ev3 = EV3Brick()

left_motor  = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor  = Motor(Port.A)            # Arm

ultrasonic = UltrasonicSensor(Port.S2) # Ultrasonic on S2
gyro       = GyroSensor(Port.S4)       # Gyro on S4

# Robot measurements (adjust if needed)
wheel_diameter = 56
axle_track = 123

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
robot.settings(straight_speed=200, turn_rate=90)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def move(distance_mm):
    """Move straight: positive = forward, negative = backward."""
    robot.straight(distance_mm)

def turn(angle):
    """
    Turn in place by *angle* degrees using the gyro.
    Positive = left, negative = right.
    Stops within 2° of the target heading.
    """
    # Current heading
    current = gyro.angle()
    target = current + angle

    # Proportional control loop
    while True:
        error = ((target - gyro.angle()) + 180) % 360 - 180
        if abs(error) < 2:          # tolerance: 2 degrees
            break
        steer = max(-90, min(90, error * 2.5))   # P-gain 2.5
        robot.drive(0, steer)
        wait(10)
    robot.stop()

def arm_down():
    """Lower the arm."""
    lift_motor.run_target(100, -10)   # down position (adjust if needed)
    wait(500)

def arm_up():
    """Raise the arm."""
    lift_motor.reset_angle(0)
    lift_motor.run_target(100, 110)  # up position
    wait(500)

# --------------------------------------------------
# Main mission
# --------------------------------------------------
def main():
   
    move(320)

    # 2. Turn left 50° (gyro accurate)
    turn(-50)

    # 3. Move forward until extremely close (≤ 30 mm)
    # VERY_CLOSE = 30   # distance in mm
    # while ultrasonic.distance() > VERY_CLOSE:
    #     robot.drive(80, 0)    # drive forward slowly
    #     wait(20)
    # robot.stop()

    # 4. Lower the arm (grab / push)
    # arm_down()

    # 5. Wait 1 second
    wait(1000)
    move(300)
    move(-400)
    turn(50)
    move(-300)

    # 6. Raise the arm
    # arm_up()

    # 7. Move backward 20 cm
   
   
    

    ev3.speaker.beep(1000, 300)
    ev3.screen.clear()

# --------------------------------------------------
# Run the mission
# --------------------------------------------------
if __name__ == "__main__":
    main()
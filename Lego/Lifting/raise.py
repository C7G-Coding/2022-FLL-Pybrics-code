#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor
from pybricks.parameters import Port

lift_motor = Motor(Port.A)

lift_motor.reset_angle(0)
lift_motor.run_target(100, 110)
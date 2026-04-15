#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()
gyro = GyroSensor(Port.S2)

gyro.reset_angle(0)

while True:
    print(gyro.angle())
    wait(1000)
    
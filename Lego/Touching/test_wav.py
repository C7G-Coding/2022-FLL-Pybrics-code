#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

ev3 = EV3Brick()

try:
    ev3.speaker.play_file("oopsy.wav")
except:
    ev3.speaker.beep()

wait(3000)
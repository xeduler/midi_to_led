#!/usr/bin/python
import time
import serial


mcu_port = "/dev/ttyACM0"
mcu_baudrate = 115200

rgb = [0, 0, 0, 150]


with serial.Serial(port = mcu_port, baudrate = mcu_baudrate, timeout = 1) as controller:
    time.sleep(3)
    colour = int(rgb[3]).to_bytes(1, "big") + int(rgb[2]).to_bytes(1, "big") + int(rgb[0]).to_bytes(1, "big") + int(rgb[1]).to_bytes(1, "big") + int(1).to_bytes(1, "big")
    controller.write(colour)
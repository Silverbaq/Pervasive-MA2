#! /usr/bin/python

import serial
from time import sleep

bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=4800 )

while True:
    print bluetoothSerial.readline()

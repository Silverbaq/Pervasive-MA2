#! /usr/bin/python

import serial
from time import sleep

bluetoothSerial = serial.Serial( "/dev/rfcomm2", baudrate=9600 )

while True:
    print bluetoothSerial.readline()

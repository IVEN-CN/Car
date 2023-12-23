import serial
import time

while 1:
    ser = serial.Serial('/dev/ttyAMA0', 9600)
    ser.write(b'1')


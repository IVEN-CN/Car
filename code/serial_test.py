import serial
import time
import RPi.GPIO as IO

ser = serial.Serial('/dev/ttyAMA0', 9600)
IO.setmode(IO.BCM)
IO.setup(18, IO.OUT)

while 1:
    IO.output(18, IO.HIGH)
    ser.write(b'1')
    time.sleep(0.25)
    IO.output(18, IO.LOW)
    time.sleep(0.25)


import serial

ser = serial.Serial('/dev/ttyAMA0', 9600)
while 1:
    data = ser.read()
    if data != None:
        print(data)
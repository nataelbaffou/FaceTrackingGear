import time
import struct
import serial
from commandesPython import Arduino
#time.sleep(5)
print("starting")

port = 'COM3'
ard = Arduino(port)

print('access port available')

xValue = 90
yValue = 90
ard.servoAttach(1, 6)
ard.servoAttach(2, 7)
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)

ard.close()

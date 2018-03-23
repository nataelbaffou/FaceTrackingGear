import time
import struct
import serial
from commandesPython import Arduino
#time.sleep(5)
print("starting")

port = 'COM3'
ard = Arduino(port)

print('access port available')

test = 90

xValue = test
yValue = test
ard.servoAttach(1, 6)
ard.servoAttach(2, 7)
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)

ard.close()

print("finished succefully")
time.sleep(2)

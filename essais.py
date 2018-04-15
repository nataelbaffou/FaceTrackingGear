import time
import struct
import serial
from commandesPython import Arduino
print("starting")

port = 'COM3'
ard = Arduino(port)

print('access port available')

test = 0
test2 = 180

ard.servoAttach(1, 6)
ard.pinMode(3, ard.OUTPUT)
ard.analogWrite(3, 255)
ard.servoAttach(2, 7)
xValue = test
yValue = test
ard.servoWrite(1, xValue)
#ard.servoWrite(2, yValue)
time.sleep(2)
xValue = test2qqqqqqqqq
yValue = test2
ard.servoWrite(1, xValue)
#ard.servoWrite(2, yValue)

ard.close()

print("finished succefully")
time.sleep(2)

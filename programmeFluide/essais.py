import time
import struct
import serial
from commandesPython import Arduino
print("starting")

port = 'COM3'
ard = Arduino(port)

print('access port available')

testX = 0
testY = 90

xValue = testX
yValue = testY
ard.servoAttach(1, 6)
ard.servoAttach(2, 7)
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)
time.sleep(2)
ard.mapping(10)
time.sleep(1)
ard.mapping(20)
time.sleep(1)
ard.mapping(30)
time.sleep(1)
ard.mapping(40)
time.sleep(1)
ard.mapping(50)
time.sleep(1)
ard.mapping(200)
time.sleep(1)


ard.close()

print("finished succefully")
time.sleep(2)

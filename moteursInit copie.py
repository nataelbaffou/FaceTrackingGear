import time
import struct
import serial
from commandesPython import Arduino
#time.sleep(5)
print("starting")

time.sleep(1)
port = 'COM5'
ard = Arduino(port)

print('access port available')

test = 0

xValue = test
yValue = test
ard.servoAttach(1, 7)
ard.servoWrite(1, xValue)
time.sleep(2)
ard.mapping(100)
time.sleep(1)
ard.mapping(240)

ard.close()

print("finished succefully")
time.sleep(2)


# -*- coding: utf-8 -*-
import serial
                
class Arduino():
    def __init__(self,port):
        
        self.ser = serial.Serial(port,baudrate=500000)

        c_recu = self.ser.read(1)
        while ord(c_recu)!=0:
            c_recu = self.ser.read(1)
        c_recu = self.ser.read(1)
        while ord(c_recu)!=255:
            c_recu = self.ser.read(1)
        c_recu = self.ser.read(1)
        while ord(c_recu)!=0:
            c_recu = self.ser.read(1)
        self.PIN_MODE = 100
        self.DIGITAL_WRITE = 101
        self.DIGITAL_READ = 102
        self.ANALOG_WRITE = 103
        self.ANALOG_READ = 104
        self.SERVO_WRITE = 105
        self.SERVO_READ = 106
        self.SERVO_ATTACH = 107
        self.MAPPING = 108
        self.STOP = 109
        self.INPUT = 0
        self.OUTPUT = 1
        self.LOW = 0
        self.HIGH = 1
        
    def close(self):
        self.ser.close()

    def pinMode(self,pin,mode):
        self.ser.write(chr(self.PIN_MODE))
        self.ser.write(chr(pin))
        self.ser.write(chr(mode))

    def digitalWrite(self,pin,output):
        self.ser.write(chr(self.DIGITAL_WRITE))
        self.ser.write(chr(pin))
        self.ser.write(chr(output))

    def digitalRead(self,pin):
        self.ser.write(chr(self.DIGITAL_READ))
        self.ser.write(chr(pin))
        x = self.ser.read(1)
        return ord(x)

    def analogWrite(self,pin,output):
        self.ser.write(chr(self.ANALOG_WRITE))
        self.ser.write(chr(pin))
        self.ser.write(chr(output))

    def analogRead(self,pin):
        self.ser.write(chr(self.ANALOG_READ))
        self.ser.write(chr(pin))
        c1 = ord(self.ser.read(1))
        c2 = ord(self.ser.read(1))
        return c1*0x100+c2

    def servoWrite(self, numServo, output):
        self.ser.write(chr(self.SERVO_WRITE))
        self.ser.write(chr(numServo))
        self.ser.write(chr(output))

    def servoAttach(self, numServo, pin):
        self.ser.write(chr(self.SERVO_ATTACH))
        self.ser.write(chr(numServo))
        self.ser.write(chr(pin))

    def mapping(self, ecartX, ecartY, invX, invY):
        self.ser.write(chr(self.MAPPING))
        precVal = 0
        for i in range(5):
            nb = 10**(5-i-1)
            newVal = int((ecartX - precVal)/nb)
            precVal = precVal + newVal * nb
            self.ser.write(chr(newVal))
        precVal = 0
        for i in range(5):
            nb = 10**(5-i-1)
            newVal = int((ecartY - precVal)/nb)
            precVal = precVal + newVal * nb
            self.ser.write(chr(newVal))
        self.ser.write(chr(invX))
        self.ser.write(chr(invY))

    def stop(self):
        self.ser.write(chr(self.STOP))
 
                

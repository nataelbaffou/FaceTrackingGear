"""
ordis
        079699370
        079699378  <----

        screen : 640 / 480

"""
import cv2
import numpy
import time
import sys
from commandesPython import Arduino
from datetime import datetime
from time import strftime

port = 'COM3'
ard = Arduino(port)

print('access port available')

xValue = 90
yValue = 90
ard.servoAttach(1, 6)
ard.servoAttach(2, 7)
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

dateNow = datetime.now()
date = str(dateNow.day) + "-" + str(dateNow.hour) + "-" + str(dateNow.minute)
number = dateNow.hour
writer = cv2.VideoWriter("videos/projet-"+str(date)+".avi", fourcc, 9.0, (640, 480))

tps = time.time()

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

cv2.namedWindow('Detection', 0)
print(face_cascade.empty())
print(cv2.__version__)
print(numpy.__version__)
time.sleep(1)
while(True):
    tpsAct = time.time() 
    ret, frame = cap.read()
    #lecture de l'image actuelle

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    height, width = frame.shape[:2]

    yScrCen = int(height/2)
    xScrCen = int(width/2)
    yScrLim = int(yScrCen/2)
    xScrLim = int(xScrCen/2)
    yScrSaf = int(height/15)
    xScrSaf = int(width/10)

    """
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (O, 0, 255), 2)
    
    """
    
    for (x,y,w,h) in faces:
                
        xFaceCen = x + int(w/2)
        yFaceCen = y + int(h/2)

        ext = 0

        xEcart = abs(xScrCen - xFaceCen)
        yEcart = abs(yScrCen - yFaceCen)

        xDep = int(xEcart*xEcart/20000)
        yDep = int(yEcart*yEcart/40000)

        xDep = int((320 - xEcart)/80)
        yDep = int((240 - yEcart)/100)
        print("x : " + str(xDep))
        print("y : " + str(yDep))
        
        if(xScrCen - xScrSaf > xFaceCen):
            xValue -= xDep
            if(xValue < 0):
                xValue = 0
        if(xScrSaf + xScrCen < xFaceCen):
            xValue += xDep
            if(xValue > 180):
                xValue = 180
        if(yScrCen - yScrSaf > yFaceCen):
            yValue -= yDep
            if(yValue < 0):
                yValue = 0
        if(yScrSaf + yScrCen < yFaceCen):
            yValue += yDep
            if(yValue > 180):
                yValue = 180

    ard.servoWrite(1, xValue)
    ard.servoWrite(2, yValue)
    
    cv2.imshow('Detection',frame)
    writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #if tpsAct > tps + 15:
    #    break

cap.release()
cv2.destroyAllWindoxScrSaf()


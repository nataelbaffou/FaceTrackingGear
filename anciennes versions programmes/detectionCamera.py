"""
ordis
        079699370
        079699378  <----

"""
import cv2
import numpy
import sys
from commandesPython import Arduino
from datetime import datetime

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
writer = cv2.VideoWriter("videos/projet-detect-"+str(date)+".avi", fourcc, 9.0, (640, 480))

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

cv2.namedWindow('Detection', 0)
print(face_cascade.empty())
print(cv2.__version__)
print(numpy.__version__)

affichage = input("taper 1 pour avoir le visuel et 2 pour ne pas l'avoir  : ")
visuel = True
if(affichage == 2):
    visuel = False

while(True):
    ret, frame = cap.read()
    #lecture de l'image actuelle

    cv2.resize(frame, None, fx=10, fy=10, interpolation = cv2.INTER_CUBIC)
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #bodies = eye_cascade.detectMultiScale(gray, 2, 5)
    height, width = frame.shape[:2]

    yScrCen = int(height/2)
    xScrCen = int(width/2)
    yScrLim = int(yScrCen/2)
    xScrLim = int(xScrCen/2)
    yScrSaf = int(height/15)
    xScrSaf = int(width/10)
    
    for (x,y,w,h) in faces:

        xFaceCen = x + int(w/2)
        yFaceCen = y + int(h/2)

        if(visuel):   
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.line(frame, (xFaceCen-10, yFaceCen), (xFaceCen+10, yFaceCen), (0,255,0), 4)
            cv2.line(frame, (xFaceCen, yFaceCen-10), (xFaceCen, yFaceCen+10), (0,255,0), 4)
        
        xEcart = abs(xScrCen - xFaceCen) - xScrSaf
        yEcart = abs(yScrCen - yFaceCen) - yScrSaf

        xDep = int(xEcart / 100) + 1
        yDep = int(yEcart /100) + 1
                
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
            if(yValue < 65):
                yValue = 65
        if(yScrSaf + yScrCen < yFaceCen):
            yValue += yDep
            if(yValue > 180):
                yValue = 180

    ard.servoWrite(1, xValue)
    ard.servoWrite(2, yValue)

    if(visuel):
        cv2.line(frame, (0, yScrCen), (width, yScrCen), (0,0,0), 2)
        cv2.line(frame, (xScrCen, 0), (xScrCen, height), (0,0,0), 2)
        cv2.line(frame, (xScrLim, yScrLim), (xScrLim, height-yScrLim), (0,0,0), 4)
        cv2.line(frame, (xScrLim, yScrLim), (width-xScrLim, yScrLim), (0,0,0), 4)
        cv2.line(frame, (width-xScrLim, height-yScrLim), (xScrLim, height-yScrLim), (0,0,0), 4)
        cv2.line(frame, (width-xScrLim, height-yScrLim), (width-xScrLim, yScrLim), (0,0,0), 4)
        cv2.line(frame, (xScrCen - xScrSaf, yScrCen - yScrSaf), (xScrCen + xScrSaf, yScrCen - yScrSaf), (0,0,0), 2)
        cv2.line(frame, (xScrCen - xScrSaf, yScrCen + yScrSaf), (xScrCen + xScrSaf, yScrCen + yScrSaf), (0,0,0), 2)
        cv2.line(frame, (xScrCen - xScrSaf, yScrCen - yScrSaf), (xScrCen - xScrSaf, yScrCen + yScrSaf), (0,0,0), 2)
        cv2.line(frame, (xScrCen + xScrSaf, yScrCen - yScrSaf), (xScrCen + xScrSaf, yScrCen + yScrSaf), (0,0,0), 2)

    
    cv2.imshow('Detection',frame)
    writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindoxScrSaf()


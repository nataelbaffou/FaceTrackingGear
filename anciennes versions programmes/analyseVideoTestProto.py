"""
ordis
        079699370
        079699378  <----

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
date = str(dateNow.month) + "/" + str(dateNow.day) + "-" + str(dateNow.hour) + "h:" + str(dateNow.minute) + "m:" + str(dateNow.second) + "s"
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
    """
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (O, 0, 255), 2)
    
    """
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        #ROI : region of interest
        roi_color = frame[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)

        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
        
        xFaceCen = x + int(w/2)
        yFaceCen = y + int(h/2)

        cv2.line(frame, (xFaceCen-10, yFaceCen), (xFaceCen+10, yFaceCen), (0,255,0), 4)
        cv2.line(frame, (xFaceCen, yFaceCen-10), (xFaceCen, yFaceCen+10), (0,255,0), 4)

        b, v, r = cv2.split(frame)
        ext = 0

        xEcart = abs(xScrCen - xFaceCen)
        yEcart = abs(yScrCen - yFaceCen)

        xDep = int((xScrCen - xScrSaf)*(xScrCen - xScrSaf)/20000)
        yDep = int((yScrCen - yScrSaf)*(yScrCen - yScrSaf)/40000)

        print(xDep)
        print(yDep)
                
        if((xScrCen - xScrSaf < xFaceCen) and (xScrSaf + xScrCen > xFaceCen) and (yScrCen - yScrSaf < yFaceCen) and (yScrSaf + yScrCen > yFaceCen)):
            ext = ext
        else:
            if(xFaceCen < xScrCen):
                xValue -= xDep
                if(xValue < 0):
                    xValue = 0
                if(xFaceCen < xScrLim):
                    ext = 1
                if(yFaceCen < yScrCen):
                    yValue -= yDep
                    if(yValue > 180):
                        yValue = 180
                    if(yFaceCen < yScrLim):
                        ext = 1
                    roi_r = r[:yScrCen, :xScrCen]
                    cv2.add(roi_r, 80, roi_r)
                else:
                    yValue += yDep
                    if(yValue < 0):
                        yValue = 0
                    if(yFaceCen > height - yScrLim):
                        ext = 1
                    
                    roi_r = r[yScrCen:, :xScrCen]
                    cv2.add(roi_r, 80, roi_r)
            else:
                xValue += xDep
                if(xValue > 180):
                    xValue = 180
                if(xFaceCen > width - xScrLim):
                    ext = 1
                if(yFaceCen < yScrCen):
                    yValue -= yDep
                    if(yValue > 180):
                        yValue = 180
                    if(yFaceCen < yScrLim):
                        ext = 1
                    
                    roi_r = r[:yScrCen, xScrCen:]
                    cv2.add(roi_r, 80, roi_r)
                else:
                    yValue += yDep
                    if(yValue < 0):
                        yValue = 0
                    if(yFaceCen > height - yScrLim):
                        ext = 1
                    
                    roi_r = r[yScrCen:, xScrCen:]
                    cv2.add(roi_r, 80, roi_r)

            if(ext == 1):
                cv2.add(b, 100, b)
                roi_b = b[yScrLim:height-yScrLim, xScrLim:width-xScrLim]
                cv2.subtract(roi_b, 100, roi_b)
            cv2.merge([b, v, r], frame)

    ard.servoWrite(1, xValue)
    ard.servoWrite(2, yValue)

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

    #if tpsAct > tps + 15:
    #    break

cap.release()
cv2.destroyAllWindoxScrSaf()


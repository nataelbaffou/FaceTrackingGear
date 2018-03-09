"""
ordis
        079699370
        079699378  <----

"""
import cv2
import numpy
import time
import sys

print("test")

cap = cv2.VideoCapture(0)
time.sleep(1)
print("2")
tps = time.time()
print("3")
#face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#test = something.load('C:/FaceTrackingGear/haarcascade_frontalface_default.xml')
#print(test)
cv2.namedWindow('Detection', 0)
print(face_cascade.empty())
print(cv2.__version__)
print(numpy.__version__)
time.sleep(1)
print("temps passe")
time.sleep(1)
while(True):
    tpsAct = time.time
    ret, frame = cap.read()
    #cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #bodies = eye_cascade.detectMultiScale(gray, 2, 5)

    """
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (O, 0, 255), 2)
    
    """
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
    
    cv2.imshow('Detection',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #if tpsAct > tps + 15:
    #    break

cap.release()
cv2.destroyAllWindows()


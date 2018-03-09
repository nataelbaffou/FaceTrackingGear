import time
import cv2
import sys
import numpy

"""
for i in range(10):
    cap = cv2.VideoCapture(i)
    print(i)
    if(cap.isOpened()):
        print("ok")
"""

video = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')

# Define an initial bounding box
bbox = (287, 23, 86, 320)

while True:

    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height, width = frame.shape[:2]
    hf = int(height/2)
    wf = int(width/2)
    hft = int(hf/1.5)
    wft = int(wf/2)
    hs = int(height/15)
    ws = int(width/10)
    ec = 20

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow('Detection',frame)

    if cv2.waitKey(1) & 0xFF == ord('t'):

        bbox = tuple(faces[0])
        continuer = True

        while continuer:

            if(continuer):

                continuer = False
                    
                # Initialize tracker with first frame and bounding box
                # change size : MedianFow, TDL
                # not : KCF, MIL

                # ATTENTION !
                """
                    SI TRACKER CHANGE :
                        -   MODIFIER CONDITION "facesDet !=" ? 
                        - ? par "()" si TLD
                        - ? par "0" et "facesDet" par "facesDet[0][0]" si KCF

                """
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init(frame, bbox)

                end = False

                nbImages = 0

                while True:
                    nbImages += 1

                    # Read a new frame
                    ok, frame = video.read()
                    frame = cv2.flip(frame, 1)

                    if not ok:
                        print('we can not read the video')
                        break
                    
                    # Update tracker
                    ok, bbox = tracker.update(frame)
                    
                    if(not ok):
                        if(not end):
                            print("end of tracking")
                            end = True
                        facesDet = face_cascade.detectMultiScale(frame, 1.2, 5)
                        print(facesDet)
                        if(facesDet != ()):
                            if(facesDet[0][0] != 0):
                                bbox = tuple(facesDet[0])
                                print("new detection : " + str(bbox))
                                continuer = True
                                break

                    if(nbImages % 10 == 0 and ok):
                        print("images = 10")
                        print(frame.shape)
                        print(bbox)
                        print(ok)
                        print(int(bbox[0]+bbox[2])-int(bbox[0]))
                        print(int(bbox[1]+bbox[3])-int(bbox[1]))
                        frameROI = frame[int(bbox[1]-ec):int(bbox[1]+bbox[3]+ec), int(bbox[0]-ec):int(bbox[0]+bbox[2]+ec)]
                        print(frameROI.shape)
                        facesDet = face_cascade.detectMultiScale(frameROI, 1.2, 5)
                        print(facesDet)
                        if(facesDet == ()):
                            facesDet = [[0,0,0,0]]
                            print("test faces Det : '" + str(facesDet[0][0]) + "'")
                        if(facesDet[0][0] == 0):
                            facesDet = face_cascade.detectMultiScale(frame, 1.2, 5)
                            if(facesDet != ()):
                                if(facesDet[0][0] != 0):
                                    new = bbox
                                    bbox = tuple(facesDet[0])
                                    continuer = True
                                    print("10 secondes worked : " + str(new))
                                    print("10 secondes is now : " + str(bbox))
                                    break
                    

                    # Draw bounding box
                    if ok:
                        x, y, w, h = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))

                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        
                        xc = x + int(w/2)
                        yc = y + int(h/2)
                        
                        cv2.line(frame, (xc-10, yc), (xc+10, yc), (0,255,0), 4)
                        cv2.line(frame, (xc, yc-10), (xc, yc+10), (0,255,0), 4)
                        b, v, r = cv2.split(frame)
                        ext = 0;
                        if(xc < wf):
                            if(xc < wft):
                                ext = 1
                            if(yc < hf):
                                if(yc < hft):
                                    ext = 1
                                roi_r = r[:hf, :wf]
                                cv2.add(roi_r, 80, roi_r)
                            else:
                                if(yc > height - hft):
                                    ext = 1
                                roi_r = r[hf:, :wf]
                                cv2.add(roi_r, 80, roi_r)
                        else:
                            if(xc > int(width-wft)):
                                ext = 1
                            if(yc < hf):
                                if(yc < hft):
                                    ext = 1
                                roi_r = r[:hf, wf:]
                                cv2.add(roi_r, 80, roi_r)
                            else:
                                if(yc > height - hft):
                                    ext = 1
                                roi_r = r[hf:, wf:]
                                cv2.add(roi_r, 80, roi_r)
                        if(ext == 1):
                            cv2.add(b, 100, b)
                            roi_b = b[hft:height-hft, wft:width-wft]
                            cv2.subtract(roi_b, 100, roi_b)
                        cv2.merge([b, v, r], frame)
                        
                    cv2.line(frame, (0, hf), (width, hf), (0,0,0), 2)
                    cv2.line(frame, (wf, 0), (wf, height), (0,0,0), 2)
                    cv2.line(frame, (wft, hft), (wft, height-hft), (0,0,0), 2)
                    cv2.line(frame, (wft, hft), (width - wft, hft), (0,0,0), 2)
                    cv2.line(frame, (width-wft, height-hft), (wft, height-hft), (0,0,0), 2)
                    cv2.line(frame, (width-wft, height-hft), (width-wft, hft), (0,0,0), 2)
                    cv2.line(frame, (wf - ws, hf - hs), (wf + ws, hf - hs), (0,0,0), 2)
                    cv2.line(frame, (wf - ws, hf + hs), (wf + ws, hf + hs), (0,0,0), 2)
                    cv2.line(frame, (wf - ws, hf - hs), (wf - ws, hf + hs), (0,0,0), 2)
                    cv2.line(frame, (wf + ws, hf - hs), (wf + ws, hf + hs), (0,0,0), 2)

                    # Display result
                    cv2.imshow("Detection", frame)
             
                    # Exit if ESC pressed
                    k = cv2.waitKey(1) & 0xff
                    if k == ord('a') :
                        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()

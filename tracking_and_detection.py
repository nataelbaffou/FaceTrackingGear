import time
import cv2
from fonctionsProg import *

demarrage = False

print("#######   FACE TRACKING GEAR   #######")
while(not demarrage):
    demarrage = True
    print("\n\nBienvenue :")
    print("Tapez 1 pour realiser un tracking")
    print("Tapez 2 pour realiser une detection")
    value = input("Votre valeur ici : ")

    technique, shapes, writing, window_mode = init()
    
    if(value == 1):
        technique = 'tracking'
    elif(value == 2):
        technique = 'detection'
    elif(value == 42):
        technique, shapes, writing, window_mode = admin_mode()
    else:
        demarrage = False
        print("Votre valeur ne correspond a aucune de nos attentes, veuillez recommencer s'il vous plait")

track = tracking('COM3', technique, window_mode, shapes, writing)

track.init_moteur()

track.init_screen_values()

# Define an initial bounding box
bbox = (287, 23, 86, 320)
ec = 20

tpsPre = time.time()
nbImages = 0
oldNbImages = 0

while True:
    frame, gray = track.image()

    faces = track.detect_faces(gray)

    for (x,y,w,h) in faces:
        track.face_center(x, y, w, h)
        
        track.add_face_lines(frame, x, y, w, h)
        
        track.calcul_deplacement()
                
        track.moove_camera()

    track.add_lines(frame)
    
    track.afficher_image(frame)
    track.writing_image(frame)

    if(faces != () and technique == 'tracking'):
        
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

                nbImages = 0
                oldNbImages = 0

                while True:
                    
                    frame, gray = track.image()
                    
                    # Update tracker
                    ok, bbox = tracker.update(frame)

                    # Do a face detection if tracker lost the person                    
                    if(not ok):
                        facesDet = track.detect_faces(gray)
                        if(facesDet != ()):
                            if(facesDet[0][0] != 0):
                                bbox = tuple(facesDet[0])
                                continuer = True
                                break

                    # Analyse if the tracker is still on the person every 10 images
                    if(nbImages % 10 == 0 and ok):
                        grayROI = gray[int(bbox[1]-ec):int(bbox[1]+bbox[3]+ec), int(bbox[0]-ec):int(bbox[0]+bbox[2]+ec)]
                        facesDet = track.detect_faces(grayROI)
                        if(facesDet == ()):
                            facesDet = [[0,0,0,0]]
                        if(facesDet[0][0] == 0):
                            facesDet = track.detect_faces(gray)
                            if(facesDet != ()):
                                if(facesDet[0][0] != 0):
                                    new = bbox
                                    bbox = tuple(facesDet[0])
                                    continuer = True
                                    break
                    

                    # Draw bounding box
                    if ok:
                        x, y, w, h = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
                        
                        track.face_center(x, y, w, h)

                        track.add_face_lines(frame, x, y, w, h)

                        track.calcul_deplacement()

                        track.moove_camera()

                    track.add_lines(frame)

                    track.afficher_image(frame)
                    track.writing_image(frame)

                    nbImages += 1
                    
                    diff  = time.time() - tpsPre
                    if(diff >= 1):
                        print(nbImages - oldNbImages)
                        oldNbImages = nbImages
                        tpsPre = time.time()
             
                    if cv2.waitKey(1) & 0xff == ord('q') :
                        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()

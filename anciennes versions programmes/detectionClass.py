"""
ordis
        079699370
        079699378  <----

"""
import cv2
import time
from fonctionsProg import *

demarrage = False

print("#######   FACE TRACKING GEAR   #######")
while(not demarrage):
    demarrage = True
    print("\n\nBienvenue :")
    print("Tapez 1 pour realiser un tracking")
    print("Tapez 2 pour realiser une detection")
    value = input("Votre valeur ici : ")

    technique, shapes, writing, window_mode, affichageTps = init()
    
    if(value == 1):
        technique = 'tracking'
    elif(value == 2):
        technique = 'detection'
    elif(value == 42):
        technique, shapes, writing, window_mode, affichageTps = admin_mode()
    else:
        demarrage = False
        print("Votre valeur ne correspond a aucune de nos attentes, veuillez recommencer s'il vous plait")

track = tracking('COM3', technique, window_mode, shapes, writing)

track.init_moteur()

track.init_screen_values()

while(True):
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

    if(affichageTps):
        is_true, ecart = track.one_second()
        if(is_true):
            print(ecart)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

track.release_all()


import time
from datetime import datetime
import cv2
from commandesPython import Arduino

"""
    Creation of tracking:
        informations needed:
            - port : port of the arduino card
            - technique : 'tracking' or 'detection'
            - mode : True for showing shapes, False else
            - window_mode : WINDOW_NORMAL or WINDOW_AUTOSIZE
"""

class tracking():
    def __init__(self, port, technique, mode, window_mode):
        self.technique = technique
        self.mode = mode
        
        self.ard = Arduino(port)
        print('access port available')
        
        self.cap = cv2.VideoCapture(0)
        print('camera available')
        
        self.xValue = 90
        self.yValue = 90

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter("videos/" + self.create_file_name(), fourcc, self.video_speed(), (640, 480))

        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        
        cv2.namedWindow('Detection', window_mode)
        
    def init_moteur(self):
        self.xValue = 90
        self.yValue = 90
        self.ard.servoAttach(1, 6)
        self.ard.servoAttach(2, 7)
        self.ard.servoWrite(1, self.xValue)
        self.ard.servoWrite(2, self.yValue)
        print('moteur initialisation succeeded')

    #def init_camera(self):

    def create_file_name(self):
        dateNow = datetime.now()
        date = dateNow.strftime("%d-%b %Hh%M")
        file_name = 'project-'
        if(self.technique == 'tracking '):
            file_name += 'track'
        elif(self.technique == 'detection '):
            file_name += 'detect'
        else:
            print('wrong value of "technique"')
        file_name += str(date) + ".avi"
        return file_name

    def video_speed(self):
        if(self.technique == 'tracking'):
            return 25
        elif(self.technique == 'detection'):
            return 9
        else:
            print('wrong value of "technique"')

track = tracking('COM3', 'tracking', False, cv2.WINDOW_NORMAL)
track.init_moteur()

print("All ended succefully")
time.sleep(5)

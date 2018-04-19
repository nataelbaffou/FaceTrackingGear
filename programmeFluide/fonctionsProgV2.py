import time
from datetime import datetime
import cv2
from commandesPython import Arduino

YLIMIT = 20
deFace = False

def init():
    #       technique / shapes / writing / window_mode /  fps / heigth / width
    return 'tracking', True,   False,  cv2.WINDOW_NORMAL, False, 20, 15

"""
    Creation of tracking:
        informations needed:
            - port : port of the arduino card
            - technique : 'tracking' or 'detection'
            - shapes : True for showing shapes, False else
            - window_mode : WINDOW_NORMAL or WINDOW_AUTOSIZE
"""

class tracking():
    def __init__(self, port, technique, window_mode, shapes, writing, rect_height, rect_width):
        self.technique = technique
        self.shapes = shapes
        self.writing = writing
        self.rect_height = rect_height
        self.rect_width = rect_width
        
        self.ard = Arduino(port)
        print('access port available')
        
        self.cap = cv2.VideoCapture(0)
        print('camera available')

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter("videos/" + self.create_file_name(), fourcc, self.video_speed(), (640, 480))

        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        
        cv2.namedWindow(self.technique, window_mode)

        self.xValue = 90
        self.yValue = 90
        self.height = 0
        self.width = 0
        self.yScrCen = 0
        self.xScrCen = 0
        self.yScrSaf = 0
        self.xScrSaf = 0
        self.xFaceCen = 0
        self.yFaceCen = 0
        self.xDep = 0
        self.yDep = 0
        self.nbImages = 0
        self.oldNbImages = 0
        self.tpsPre = time.time()
        
    def init_moteur(self):
        self.xValue = 90
        self.yValue = 90
        self.ard.servoAttach(1, 6)
        self.ard.servoAttach(2, 7)
        self.ard.servoWrite(1, self.xValue)
        self.ard.servoWrite(2, self.yValue)
        print('moteur initialisation succeeded')

    def init_screen_values(self):
        _, frame = self.cap.read()
        self.height, self.width = frame.shape[:2]
        self.height = int(self.height/1)
        self.width = int(self.width/1)
        self.yScrCen = int(self.height/2)
        self.xScrCen = int(self.width/2)
        self.yScrSaf = int(self.height/self.rect_height)
        self.xScrSaf = int(self.width/self.rect_width)

    def image(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        #size = (self.width, self.height)
        #frame = cv2.resize(frame, size, interpolation = 3)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return (frame, gray)

    def detect_faces(self, gray):
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces

    def face_center(self, x, y, w, h):
        self.xFaceCen = x + int(w/2)
        self.yFaceCen = y + int(h/2)

    def calcul_deplacement(self):
        xEcart = abs(self.xScrCen - self.xFaceCen)
        # - self.xScrSaf
        yEcart = abs(self.yScrCen - self.yFaceCen)
        # - self.yScrSaf

        self.xDep = int(xEcart / 50) + 1
        self.yDep = int(yEcart /50) + 1

        self.xDep = xEcart
        self.yDep = yEcart

    def moove_camera(self):
        """
        if(self.xScrCen - self.xScrSaf > self.xFaceCen):
            self.xValue += self.xDep
            if(self.xValue > 180):
                self.xValue = 180
        if(self.xScrSaf + self.xScrCen < self.xFaceCen):
            self.xValue -= self.xDep
            if(self.xValue < 0):
                self.xValue = 0
        if(self.yScrCen + self.yScrSaf < self.yFaceCen):
            self.yValue -= self.yDep
            if(self.yValue < 90-YLIMIT):
                self.yValue = 90-YLIMIT
        if(self.yScrCen - self.yScrSaf > self.yFaceCen):
            self.yValue += self.yDep
            if(self.yValue > 90+YLIMIT):
                self.yValue = 90+YLIMIT

        self.ard.servoWrite(1, self.xValue)
        self.ard.servoWrite(2, self.yValue)
        """
        invX = 1
        invY = 1
        if(self.xScrCen < self.xFaceCen):
            invX = 0
        if(self.yScrCen < self.yFaceCen):
            invY = 0
        self.ard.mapping(self.xDep, self.yDep, invX, invY)
        

    def add_face_lines(self, frame, x, y, w, h):
        if(self.shapes):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #cv2.line(frame, (self.xFaceCen-10, self.yFaceCen), (self.xFaceCen+10, self.yFaceCen), (0,255,0), 4)
            #cv2.line(frame, (self.xFaceCen, self.yFaceCen-10), (self.xFaceCen, self.yFaceCen+10), (0,255,0), 4)
            
    def add_lines(self, frame):
        if(self.shapes):
            cv2.line(frame, (0, self.yScrCen), (self.width, self.yScrCen), (0,0,0), 2)
            cv2.line(frame, (self.xScrCen, 0), (self.xScrCen, self.height), (0,0,0), 2)
            cv2.line(frame, (self.xScrCen - self.xScrSaf, self.yScrCen - self.yScrSaf), (self.xScrCen + self.xScrSaf, self.yScrCen - self.yScrSaf), (0,0,0), 2)
            cv2.line(frame, (self.xScrCen - self.xScrSaf, self.yScrCen + self.yScrSaf), (self.xScrCen + self.xScrSaf, self.yScrCen + self.yScrSaf), (0,0,0), 2)
            cv2.line(frame, (self.xScrCen - self.xScrSaf, self.yScrCen - self.yScrSaf), (self.xScrCen - self.xScrSaf, self.yScrCen + self.yScrSaf), (0,0,0), 2)
            cv2.line(frame, (self.xScrCen + self.xScrSaf, self.yScrCen - self.yScrSaf), (self.xScrCen + self.xScrSaf, self.yScrCen + self.yScrSaf), (0,0,0), 2)

    def afficher_image(self, frame):
        if(deFace):
            frame = cv2.flip(frame, 1)
        cv2.imshow(self.technique,frame)
        self.add_image()

    def writing_image(self, frame):
        if(self.writing):
            self.writer.write(frame)
    
    def release_all(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.ard.close()
        
    def create_file_name(self):
        dateNow = datetime.now()
        date = dateNow.strftime("%d-%b %Hh%M")
        file_name = 'project-'
        if(self.technique == 'tracking'):
            file_name += 'track '
        elif(self.technique == 'detection'):
            file_name += 'detect '
        else:
            print('wrong value of "technique"')
        file_name += str(date) + ".avi"
        return file_name

    def video_speed(self):
        if(self.technique == 'tracking'):
            return 29
        elif(self.technique == 'detection'):
            return 14
        else:
            print('wrong value of "technique"')

    def add_image(self):
        self.nbImages += 1

    def one_second(self):
        diff  = time.time() - self.tpsPre
        if(diff >= 1):
            ecart = self.nbImages - self.oldNbImages
            self.oldNbImages = self.nbImages
            self.tpsPre = time.time()
            return True, ecart
        else:
            return False, None
    

def admin_mode():
    paramText = ['TECHNIQUE', 'SHAPES', 'WRITING', 'WINDOW_MODE', 'AFFICHAGE DES FPS', 'TAILLE RECTANGLE HEIGHT', 'TAILLE RECTANGLE WIDTH']
    modif = [['tracking', 'detection'], [False, True], [False, True], [cv2.WINDOW_NORMAL, cv2.WINDOW_AUTOSIZE], [False, True]]
    param = list(init())
    print("\n\n#######   ATTENTION   #######\n\nVous venez d'entrer dans le mode administrateur !!")
    continuer = True
    print("\n\nQuelle technique souhaitez-vous employer ?\nTapez 1 pour realiser un tracking")
    print("Tapez 2 pour realiser une detection")
    value = input("Votre valeur ici : ")
    if(value == 2):
        param[0] = 'detection'
    while(continuer):
        print("\n\nVous pouvez modifier les parametres suivants :\n")
        print("     - [1] technique :   {}\n".format(param[0])\
            + "     - [2] shapes :      {}\n".format(param[1])\
            + "     - [3] writing :     {}\n".format(param[2])\
            + "     - [4] window_mode : {}\n".format(param[3])\
            + "     - [5] affich fps :  {}\n".format(param[4])\
            + "     - [_] taille rect :\n"\
            + "             - [6] height : {}\n".format(param[5])\
            + "             - [7] width  : {}\n".format(param[6]))
        choice = int(input("\n(Tapez le chiffre correspondant ou '0' pour quitter)\nQuelle valeur voulez-vous modifier ? : "))
        if(choice == 0):
            continuer = False
        elif(choice < 1 or choice > 7):
            print("\n\nLa valeur ecrite ne correspond a aucune des valeurs demandees, veuillez recommencer")
        else:
            print("\n\n#######   MODIFICATION DE '{}'   #######\n\n".format(paramText[choice-1]))
            if(choice == 6 or choice == 7):
                mot = choice == 6 and 'hauteur' or 'largeur'
                print("     - Entrez n'importe quelle valeur entiere positive, elle divisera la " + mot)

                value = int(input("\n\nVotre choix : "))

                print("\nAncienne valeur du parametre '{2}' : '{0}'\nNouvelle valeur du parametre '{2}' : '{1}'".format(param[choice-1], value, paramText[choice-1].lower()))
                param[choice-1] = value
            else:
                print("Ce parametre peut prendre les valeurs suivantes : \n")
                if(choice == 1):
                    print("     - [0] tracking mode\n     - [1] detection mode")
                elif(choice == 2):
                    print("     - [0] image without shapes\n     - [1] image with shapes")
                elif(choice == 3):
                    print("     - [0] doesn't write the file\n     - [1] write the file")
                elif(choice == 4):
                    print("     - [0] normal window (resizable)\n     - [1] autosize window (not resizable)")
                elif(choice == 5):
                    print("     - [0] doesn't print the number of images per second\n     - [1] print the number of images per second")
                value = input("\n\nVotre choix : ")

                print("\nAncienne valeur du parametre '{2}' : '{0}'\nNouvelle valeur du parametre '{2}' : '{1}'".format(param[choice-1], modif[choice-1][value], paramText[choice-1].lower()))
                param[choice-1] = modif[choice-1][value]

    print("\n\nValeurs finales des parametres :\n"\
        + "     - technique :   {}\n".format(param[0])\
        + "     - shapes :      {}\n".format(param[1])\
        + "     - writing :     {}\n".format(param[2])\
        + "     - window_mode : {}\n".format(param[3])\
        + "     - affich fps :  {}\n".format(param[4])\
        + "     - taille rect :\n"\
        + "             - height : {}\n".format(param[5])\
        + "             - width  : {}\n".format(param[6]))

    return param

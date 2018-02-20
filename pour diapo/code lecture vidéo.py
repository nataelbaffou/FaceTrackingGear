import cv2

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)

# Création d'une fenêtre pour afficher le rendu
cv2.namedWindow('Detection', 0)

# Répéter la lecture
while(True):

    # Lecture de l'image actuelle
    ret, frame = cap.read()
    
    # Affichage de l'image actuelle
    cv2.imshow('Detection',frame)

# Suppression de la lecture vidéo et de l'affichage de la fenêtre
cap.release()
cv2.destroyAllWindoxScrSaf()


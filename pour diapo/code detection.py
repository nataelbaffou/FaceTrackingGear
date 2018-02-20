# Initialisation

# Choix de l'objet à détecter
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')


while(True):

    """
        Lecture de l'image
        + quelques modifications sur l'image
    """

    # Détection du ou des visages sur l'image sélectionnée
    faces = face_cascade.detectMultiScale(image, 1.3, 5)


    # Ajout ou non d'affichage sur l'image (contour des visages...)

    
    # Affichage
    cv2.imshow('Detection',frame)

# Fin


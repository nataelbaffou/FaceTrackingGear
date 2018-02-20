# Initialisation

# Choix de l'objet à détecter
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')

while True:

    """
        Une boucle jusqu'à détecter un premier visage
    """

    
    # Si un visage est détecté on commence le tracking
    if(faces != ()):
        
        # On initialise le placement du visage
        bbox = tuple(faces[0])
        continuer = True

        while continuer:
                

                # On initialise le tracker
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init(frame, bbox)

                while True:
                    
                    # Lecture d'une nouvelle image
                    
                    # Mise à jour du tracker
                    ok, bbox = tracker.update(frame)
                    
                    """
                        On vérifie si l'image n'a pas été perdue

                        On ajoute si besoin les contours des visages et autres affichages
                    """
                    
                    # On affiche les résultats
                    cv2.imshow("Detection", frame)

# Fin
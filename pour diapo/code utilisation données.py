"""

    Initialisation

    + réalisation d'un algorithme de tracking ou de détection

"""


"""
    
    On calcul en fonction de l'algorithme les deux valeurs ci-dessous
    les coordonnées du centre du visage:

    xFaceCen
    YFaceCen
    
"""

# On calcul alors l'écart sur les deux axes
xEcart = abs(xScrCen - xFaceCen) - xScrSaf
yEcart = abs(yScrCen - yFaceCen) - yScrSaf

# On calcul alors les déplacement des moteurs sur les deux axes
xDep = int(xEcart / 100) + 1
yDep = int(yEcart /100) + 1

"""

    On modifie les valeurs correspondant
    a la position des moteurs

"""

# On bouge les moteurs
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)

# Affichage des images

# Fin

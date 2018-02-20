from commandesPython import Arduino

# Initialisation du port où est positionner la carte
port = 'COM3'
ard = Arduino(port)

xValue = 90
yValue = 90
ard.servoAttach(1, 6)
ard.servoAttach(2, 7)
ard.servoWrite(1, xValue)
ard.servoWrite(2, yValue)

"""
    *** CODE ***
    Initialisation de certaines valeurs
"""

while(True):
    
    """
        *** CODE ***
        Ensemble du code de détection ou tracking
    """

    # Contôle des moteurs après définition des valeurs respectives en degrés
    ard.servoWrite(1, xValue)
    ard.servoWrite(2, yValue)

    
    cv2.imshow('Detection',frame)


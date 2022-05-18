import numpy as np
import cv2 as cv
import sys

# Inserisci 1 e connetti la videocamera al computer tramite USB
# se non funziona prova tutte le porte USB lanciando questo script.
KEY_USB = 1

cap = cv.VideoCapture(KEY_USB)
#cap = cv.VideoCapture('/media/dev1')

# testa se la videocamera è connessa
if not cap.isOpened():
    print("Cannot open camera")
    exit()

def rescale_frame(frame, percent=75):
    '''
    riscala l'immagine della videocamera in base ad una percentuale. 
    percent = 100 ,  1 : 1    non cambi la dimensione.
    percent = 150 ,  1 : 1.5  scali di una volta e mezzo
    percent = 50  ,  1 : 0.5  scali di mezza volta
    '''
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)

i = 0

while True:
    #cattura frame per frame dalla videocamera
    ret, frame = cap.read()
    # se ret non è uguale a True, esci dall'loop
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # riscala frame di una percentuale
    frame_modified = rescale_frame(frame, percent=450)
    cv.imshow('frame', frame_modified )

    if cv.waitKey(1) & 0xFF == ord('s'): #save on pressing 'y' 
        cv.imwrite(sys.path[0]+"/foto_"+str(i)+".png",frame_modified) 
        i=i+1
    
    # esci premento c 
    if cv.waitKey(1) == ord('c'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
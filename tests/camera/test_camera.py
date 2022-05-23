import numpy as np
import cv2 as cv
import sys
from time import sleep
import argparse
import cv2

''' IMPORTANTE
python3 camera.py 2

questo programma deve essere avviato dando il numero della porta usb connessa come parametro da terminale

'''

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

def main(usb_port=0):
    '''
    connettiti alla videocamera attraverso la porta usb attraverso la libreria di opencv.
    scatta una foto ogni volta che premi il tasto S
    salva la foto nella sottocartella ./img
    '''
    # porta usb passata come argomento da linea di comando, come nella line successiva: 
    # python3 .\tests\camera\camera.py 0
    parser = argparse.ArgumentParser()
    parser.add_argument('usb', type=int)
    args = parser.parse_args()

    # Inserisci 1 e connetti la videocamera al computer tramite USB
    # se non funziona prova tutte le porte USB lanciando questo script.
    # KEY_USB = 0
    KEY_USB = args.usb

    # inizializza l'oggetto videocamera
    cap = cv.VideoCapture(KEY_USB)

    # contatore salva foto
    i = 0
    
    sleep(1)
    INTERVALLO_SECONDI = 10
    i=0
    while True:
        #cattura frame per frame dalla videocamera
        ret, frame = cap.read()
        # se ret non è uguale a True, esci dall'loop
        #if not ret:
        #    print("impossible ricevere immagini dalla videocamera")
        #    continue

        # riscala frame di una percentuale
       # frame_modified = rescale_frame(frame, percent=450)
        
        #if np.array(frame).any(): 
        cv.imshow('frame', frame )

        i+=1
        sleep(INTERVALLO_SECONDI)
        cv2.imwrite(sys.path[0]+"/img/term/foto_"+str(i)+".png",frame) 

        # se premi il tasto C salvi una foto
        if cv.waitKey(1) & 0xFF == ord('s'): #save on pressing 'y' 
            cv.imwrite(sys.path[0]+"/img/foto_"+str(i)+"_"+str(KEY_USB)+".png",frame) 
            i=i+1
            sleep(0.1)


    # rilascia la videocamera quando esci dal programma
    #cap.release()
    #cv.destroyAllWindows()

    # testa se la videocamera è connessas
    #if not cap.isOpened():
    #    print("Cannot open camera")
    #    exit()
        
if __name__ == "__main__":
    main()
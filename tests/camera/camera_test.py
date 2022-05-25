import numpy as np
import cv2 as cv
import sys
from time import sleep
import argparse
import cv2

# esempio di come lanciare lo script                      
# python3 camera.py --porta_usb 2 --nome_cartella "viz" --intervallo_secondi 4


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


parser = argparse.ArgumentParser(description='Test fotografie ad intervalli regolari con tutti i tipi di videocamere disponibili per OpenCV')

parser.add_argument('--porta_usb', type=int, required=True , default=1, help="numero porta usb del dispositivo")                      # ID PORTA USB DISPOSITIVO
parser.add_argument('--nome_cartella', type=str, required=True, default="viz", help="nome cartella esistente dentro img/ dove salvare le foto")                 # nome cartella img in cui salvare le foto
parser.add_argument('--intervallo_secondi', type=int,default = 4 , help="intervallo di secondi fra 2 fotografie")     

args = parser.parse_args()

# Inserisci 1 e connetti la videocamera al computer tramite USB
# se non funziona prova tutte le porte USB lanciando questo script.
# KEY_USB = 0
KEY_USB = args.porta_usb
CARTELLA = args.nome_cartella
INTERVALLO_SECONDI = args.intervallo_secondi

# inizializza l'oggetto videocamera
cap = cv.VideoCapture(KEY_USB)
sleep(1)

# contatore salva foto
i = 0

while True:
    #cattura frame per frame dalla videocamera
    ret, frame = cap.read()
    # se ret non è uguale a True, esci dall'loop
    if not ret:
        print("impossible ricevere immagini dalla videocamera")
        sleep(2)

    # frame_modified = rescale_frame(frame, percent=450)

    if np.array(frame).any(): 
        cv.imshow('frame', frame )
        i+=1
        cv2.imwrite(sys.path[0]+"/img/"+CARTELLA+"/foto_"+str(i)+".png",frame) 
        sleep(INTERVALLO_SECONDI)
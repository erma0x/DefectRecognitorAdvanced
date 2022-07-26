#!/usr/bin/env python

# librerie built-in
import sys
import os
import os.path

import time
import socket
from datetime import datetime
from copy import deepcopy
import argparse

# librerie di terze parti
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from colorama import Fore, Back, Style

from PIL import Image
import cv2
 
# moduli del progetto
from utils.params import *

def empty(a):
    pass

def gamma_trans(img, gamma):
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)]
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img,gamma_table)

def zoom_at(img, x, y, zoom):
    w, h = img.size
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2, 
                    x + w / zoom2, y + h / zoom2))
    return img.resize((w, h), Image.LANCZOS)

def main():

    videocamera = cv2.VideoCapture(KEY_USB)
    fattore_bassa_risoluzione = 1.0 
    
    # risoluzione 12.3 MegaPixels
    videocamera.set(3, RISOLUZIONE[0] / fattore_bassa_risoluzione) 
    videocamera.set(4, RISOLUZIONE[1] / fattore_bassa_risoluzione) 

    ricetta = {}

    ##################################################################################
    # PARAMETRI LINEA DI COMANDO
    ROOT_PATH = sys.path[0]
    id_immagini_salvate = []
    contatore_foto = 0
    numero_frame = 0
    n_experiment = 0
    true_values = ("True","t","T",True,'true')

    ap = argparse.ArgumentParser()

    ap.add_argument('-s', '--save',default=True, required=False,
                    help = 'save the frames') 

    ap.add_argument('-v', '--visualize', default=False , required=False,
                    help = 'visualize frames on panel')

    ap.add_argument('-w', '--weights', default = "yolo_defects.pt", required=False,
                    help = 'path to yolo pre-trained weights')

    ap.add_argument('-c', '--classes', default = "classes.txt", required=False,
                    help = 'path to text file containing class names')

    ap.add_argument('-n', '--number_experiment', default = 0 , required=False,
                    help = 'number of experiment')

    args = ap.parse_args()

    ################################################################################
    # ESTETICA stampa logo, descrizione ed introduzione
    print(Fore.CYAN + LOGO + Style.RESET_ALL + '\n'+ descrizione )
    print('\n🚀 Computer Vision App '+ Fore.GREEN  +'[start]' + Style.RESET_ALL)
    

    while True:
        #try:
        # PANNELLI DI VISUALIZZAZIONE e DI CONTROLLO
        # crea interfaccia per visualizzare i risultati
        cv2.namedWindow(nome_pannello_di_visualizzazione)
        cv2.resizeWindow(nome_pannello_di_visualizzazione, RISOLUZIONE[0], RISOLUZIONE[1])

        #crea panello di controllo
        cv2.namedWindow(nome_pannello_di_controllo)
        cv2.resizeWindow(nome_pannello_di_controllo, RISOLUZIONE[0], RISOLUZIONE[1])

        # inizializza la trackbar con i vari parametri ed i loro massimi o minimi
        cv2.createTrackbar("fps", nome_pannello_di_controllo, 1, 20, empty)
        cv2.setTrackbarMin('fps', nome_pannello_di_controllo, 1)
        cv2.createTrackbar("gamma", nome_pannello_di_controllo, 100, 200, empty)
        cv2.setTrackbarMin('gamma', nome_pannello_di_controllo, 1)
        cv2.createTrackbar("size_frame_x", nome_pannello_di_controllo, 800, 2400, empty)
        cv2.setTrackbarMin('size_frame_x', nome_pannello_di_controllo, 200)
        cv2.createTrackbar("size_frame_y", nome_pannello_di_controllo, 400, 1080, empty)
        cv2.setTrackbarMin('size_frame_y', nome_pannello_di_controllo, 100)


        FPS = cv2.getTrackbarPos("fps", nome_pannello_di_controllo)        
        print('📷 videocamera '+ Fore.GREEN + '\n\t online' + Style.RESET_ALL)
        print(Fore.GREEN + '\n\t resolution \t' + str(RISOLUZIONE[0]) + 'x' + str(RISOLUZIONE[1]) + Style.RESET_ALL)
        print(Fore.GREEN + '\n\t fps \t' + str(FPS) + Style.RESET_ALL)

        
        ########################################
        IP_SERVER = socket.gethostname()
        ########################################
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.bind((IP_SERVER,PORTA_SERVER))
        print("Server in ascolto al seguente indirizzo : " + IP_SERVER + ":" + str(PORTA_SERVER))
          

        while videocamera.isOpened():

            FPS = cv2.getTrackbarPos("fps", nome_pannello_di_controllo)
            video_gamma = cv2.getTrackbarPos("gamma", nome_pannello_di_controllo)
            video_size_x = cv2.getTrackbarPos("size_frame_x", nome_pannello_di_controllo)
            video_size_y = cv2.getTrackbarPos("size_frame_y", nome_pannello_di_controllo)


            # image_gamma_correct = gamma_trans(frame, video_gamma/100)
            #cv2.imshow(nome_pannello_di_visualizzazione, image_gamma_correct)

            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     videocamera.release()
            #     cv2.destroyAllWindows()
            #     break

            payload, client_address = mySocket.recvfrom(1024)

            if 'f' in str(payload)[2]:
                id_pezzo = str(payload)[1:].replace("'","").split(",")[1]
                
                isWritten = False

                t1 = datetime.now()

                check, frame = videocamera.read()
            
                frame = cv2.resize(frame, (video_size_x, video_size_y), fx = 0, fy = 0, interpolation = cv2.INTER_CUBIC)
                

                if args.save in true_values and type(frame) != type(None):
                    path_folder = ROOT_PATH +'/run/experiment_' + str(n_experiment)
                    path_file = path_folder +'/foto_'+str(id_pezzo)+'.png'
                    
                    if not os.path.exists(path_folder):
                        os.makedirs(ROOT_PATH +'/run/experiment_' + str(n_experiment))
                        path_file = path_folder +'/foto_'+str(id_pezzo)+'.png'
                        if id_pezzo in id_immagini_salvate:
                            path_file = path_file.replace('.png','_' + str(numero_frame) + '.png')
                            while os.path.isfile(path_file):
                                numero_frame += 1
                                path_file = path_file.replace('.png','_' + str(numero_frame) + '.png')
                            
                            isWritten = cv2.imwrite(path_file, frame)

                        else:
                            isWritten = cv2.imwrite(path_file, frame)
                    else:
                        while os.path.isfile(path_file):
                            numero_frame += 1
                            path_file = path_file.replace('.png','_' + str(numero_frame) + '.png')
                        isWritten = cv2.imwrite(path_file, frame)

                    id_immagini_salvate.append(id_pezzo)

                    contatore_foto += 1

                    if isWritten:
                        t2 = datetime.now()
                        print('immagine salvata con successo')
                        print('tempo di salvataggio: ' + str(t2-t1))

            #time.sleep(1/FPS) 

if __name__ == "__main__":
    main()

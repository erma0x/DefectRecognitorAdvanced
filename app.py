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
import depthai as dai
 
# moduli del progetto
import utils.systematik_opencv as systematik
from utils.params import PORTA_SERVER, IP_SERVER, IP_PLC, PORTA_PLC
from utils.ricette import ricetta_default
from utils.estetica import LOGO, descrizione, nome_pannello_di_controllo, nome_pannello_di_visualizzazione


def empty(a):
    pass


def main():
    '''
        numero esperimento


    Applicazione di Computer Vision
    1. inizializza il server
    2. aspetta il messaggio da client plc con socket con ID ricetta e ID pezzo
    3. scatta una foto e salvala
    4. elabora la foto rilevando i difetti
    5. ritorna la foto elaborata in una cartella
    6. ritorna lo status (presenza di errori) e l'ID del pezzo
    '''

    KEY_USB = 2 # porta USB videocamera
    # inizializza l'oggetto videocamera
    videocamera = cv2.VideoCapture(KEY_USB)
    
    # risoluzione 12.3 MegaPixels
    fattore_bassa_risoluzione = 10

    videocamera.set(3, 4295/fattore_bassa_risoluzione)  # Set horizontal resolution
    videocamera.set(4, 2864/fattore_bassa_risoluzione)  # Set vertical resolution

    ########################################################################################
    # PARAMETRI
    ricetta = {} # parametri per scattare la foto ed elaborarla
    ROOT_PATH = sys.path[0]
    n_experiment = 0
    id_immagini_salvate = []
    contatore_foto = 0
    numero_frame = 1

    ##################################################################################
    # PARAMETRI LINEA DI COMANDO
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
    # ESTRAI I PARAMETRI DELLA RICETTA_DEFAULT
    fps = ricetta_default['fps']                
    
    video_size_x = ricetta_default['video_size_x']                
    video_size_y = ricetta_default['video_size_y']

    manual_focus_parameter = ricetta_default['manual_focus_parameter']                
    exposition = ricetta_default['exposition']                
    iso = ricetta_default['iso']

    # canny_x = ricetta_default['canny_x']                
    # canny_y = ricetta_default['canny_y']  

    # line_x = ricetta_default['line_x']                
    # line_y = ricetta_default['line_y']                
    # line_z = ricetta_default['line_z']

    cartoonize_x = ricetta_default['cartoonize_x']                
    cartoonize_y = ricetta_default['cartoonize_y']                
    cartoonize_z = ricetta_default['cartoonize_z']
    
    hsv_1_x = ricetta_default['hsv_1_x'] 
    hsv_1_y = ricetta_default['hsv_1_y']
    hsv_1_z = ricetta_default['hsv_1_z']
    hsv_2_x = ricetta_default['hsv_2_x']
    hsv_2_y = ricetta_default['hsv_2_y']
    hsv_2_z = ricetta_default['hsv_2_z']

    # min_canny_a = ricetta_default['min_canny_a']                
    # max_canny_a = ricetta_default['max_canny_a']     
    # min_canny_b = ricetta_default['min_canny_b']     
    # max_canny_b = ricetta_default['max_canny_b']      
    ################################################################################


    ################################################################################
    # ESTETICA stampa logo, descrizione ed introduzione
    print(Fore.CYAN + LOGO + Style.RESET_ALL + '\n'+ descrizione )
    print('\n🚀 Computer Vision App '+ Fore.GREEN  +'[start]' + Style.RESET_ALL)
    ################################################################################

    while True:
        #try:
        ################################################################################
        # PANNELLI DI VISUALIZZAZIONE e DI CONTROLLO
        # crea interfaccia per visualizzare i risultati
        cv2.namedWindow(nome_pannello_di_visualizzazione)
        cv2.resizeWindow(nome_pannello_di_visualizzazione, video_size_x, video_size_y)

        # crea panello di controllo
        cv2.namedWindow(nome_pannello_di_controllo)
        cv2.resizeWindow(nome_pannello_di_controllo, video_size_x, video_size_y)

        #if args.visualize in ('True',True,'T','t'):

        # inizializza la trackbar con i vari parametri ed i loro massimi o minimi
        cv2.createTrackbar("fps", nome_pannello_di_controllo, 0, 20, empty)
        cv2.createTrackbar("exposition", nome_pannello_di_controllo, 0, 55000, empty)
        cv2.createTrackbar("iso", nome_pannello_di_controllo, 0, 500, empty)
        cv2.createTrackbar("focus", nome_pannello_di_controllo, 0, 1000, empty)

        # cv2.createTrackbar("canny_x", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("canny_y", nome_pannello_di_controllo, 0, 255, empty)

        cv2.createTrackbar("cartoon_x", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("cartoon_y", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("cartoon_z", nome_pannello_di_controllo, 0, 255, empty)

        # cv2.createTrackbar("line_x", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("line_y", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("line_z", nome_pannello_di_controllo, 0, 255, empty)

        cv2.createTrackbar("hsv_1_x", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("hsv_1_y", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("hsv_1_z", nome_pannello_di_controllo, 0, 255, empty)

        cv2.createTrackbar("hsv_2_x", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("hsv_2_y", nome_pannello_di_controllo, 0, 255, empty)
        cv2.createTrackbar("hsv_2_z", nome_pannello_di_controllo, 0, 255, empty)

        # cv2.createTrackbar("min_canny_a", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("max_canny_a", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("min_canny_b", nome_pannello_di_controllo, 0, 255, empty)
        # cv2.createTrackbar("max_canny_b", nome_pannello_di_controllo, 0, 255, empty)

        ################################################################################


        print('📷 videocamera '+ Fore.GREEN + '\t[online]' + Style.RESET_ALL)


        ################################################################################
        # SOCKET
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket server basato su IPv4 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP_SERVER,PORTA_SERVER))

        #s.connect((IP_PLC,PORTA_PLC))

        #except:
        #    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Listening on " + IP_SERVER + ":" + str(PORTA_SERVER))

        # il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)
        
        
        # accetta connessioni da uno specifico indirizzo
        #connection, addr = s.accept()
        #print(f"🛰️  connesso con macchina PLC con IP :  " + Fore.YELLOW + addr[0] + ':' + str(addr[1]) + Style.RESET_ALL )
        #s.listen(PORTA_SERVER)

        while True:

            payload, client_address = sock.recvfrom(1024)

            print("Messaggio ricevuto da : " + str(client_address[0])+':'+str(client_address[1]), " messaggio ",payload)


            # fare attivare da qua sotto lo script
            # filtro per la PLC, se i dati contengono come primo carattere 'f' fai una foto
            if 'f' in str(payload)[2]: 

                #connection.close()
                id_pezzo = str(payload)[1:].replace("'","").split(',')[1]

                print('\n📡 dati ricevuti da PLC: ' + Fore.BLUE  + str(payload)  + Style.RESET_ALL + ' id pezzo' ,id_pezzo)

                try:
                    # ottieni un immagine dalla videocamera
                    check, frame = deepcopy(videocamera.read())                
                    print('📷'+ Fore.GREEN + 'taking photo' + Style.RESET_ALL,'\n')

                    if type(frame) == type(None) or not check:
                        print("Errore : non e'possibile scattare fotografie ")
                        break
                    
                    if not videocamera:
                        print("Errore : inizializzazione errata dell'oggetto videocamera")

                except:
                    print('💀'+Fore.RED+' [errore]'+  Style.RESET_ALL+' | impossibile ottenere il frame dalla videocamera')

                ################################################################################
                #PARAMETRI TRACKBAR RICETTA
                # ottieni i valori dalla trackbar
                ricetta['fps'] = cv2.getTrackbarPos("fps", nome_pannello_di_controllo)
                ricetta['exposition'] = cv2.getTrackbarPos("exposition", nome_pannello_di_controllo)
                ricetta['iso'] = cv2.getTrackbarPos("iso", nome_pannello_di_controllo)
                ricetta['focus'] = cv2.getTrackbarPos("focus", nome_pannello_di_controllo)

                ricetta['canny_x'] = cv2.getTrackbarPos("canny_x", nome_pannello_di_controllo)
                ricetta['canny_y'] = cv2.getTrackbarPos("canny_y", nome_pannello_di_controllo)

                ricetta['line_x'] = cv2.getTrackbarPos("line_x", nome_pannello_di_controllo)
                ricetta['line_y'] = cv2.getTrackbarPos("line_y", nome_pannello_di_controllo)
                ricetta['line_z'] = cv2.getTrackbarPos("line_z", nome_pannello_di_controllo)

                ricetta['cartoon_x'] = cv2.getTrackbarPos("cartoon_x", nome_pannello_di_controllo)
                ricetta['cartoon_y'] = cv2.getTrackbarPos("cartoon_y", nome_pannello_di_controllo)
                ricetta['cartoon_z'] = cv2.getTrackbarPos("cartoon_z", nome_pannello_di_controllo)

                ricetta['hsv_1_x'] = cv2.getTrackbarPos("hsv_1_x", nome_pannello_di_controllo)
                ricetta['hsv_1_y'] = cv2.getTrackbarPos("hsv_1_y", nome_pannello_di_controllo)
                ricetta['hsv_1_z'] = cv2.getTrackbarPos("hsv_1_z", nome_pannello_di_controllo)

                ricetta['hsv_2_x'] = cv2.getTrackbarPos("hsv_2_x", nome_pannello_di_controllo)
                ricetta['hsv_2_y'] = cv2.getTrackbarPos("hsv_2_y", nome_pannello_di_controllo)
                ricetta['hsv_2_z'] = cv2.getTrackbarPos("hsv_2_z", nome_pannello_di_controllo)

        
                ################################################################################


                ##################################################################################
                # 🤖 COMPUTER VISION
                # i parametri modificati nel pannello di controllo con le trackbar vengono aggiornati ogni frame
                #frame = video_frame.getCvFrame() # ottieni il frame da videocamere luxonis

                try:
                    frame_elaborato = systematik.computer_vision_system(frame, params = ricetta)
                    
                    if args.visualize in ('True',True,'T','t'):

                        cv2.imshow(nome_pannello_di_visualizzazione, frame_elaborato)
                        cv2.waitKey(1)
                
                except:
                    pass
                ##################################################################################


                ##################################################################################
                # SALVA LA FOTO
                if type(frame) == type(None):
                    if not os.path.exists(ROOT_PATH +'/run/exp' + str(n_experiment)):
                        os.makedirs(ROOT_PATH +'/run/exp' + str(n_experiment))

                    if args.save in ('True',True):
                        path_file = ROOT_PATH +'/run/exp' + str(n_experiment)+'/foto'+str(id_pezzo)+'.png'

                        if id_pezzo in id_immagini_salvate:
                            new_path = path_file.replace('.png','_' + str(numero_frame) + '.png')
                            if os.path.isfile(new_path):
                                while os.path.isfile(new_path):
                                    numero_frame += 1
                                    new_path = path_file.replace('.png','_' + str(numero_frame) + '.png')
                                cv2.imwrite(new_path, frame)

                            else:
                                cv2.imwrite(new_path, frame)
                        else:  
                            cv2.imwrite(path_file, frame)

                        ##################################################################################

                        id_immagini_salvate.append(id_pezzo)
                        contatore_foto += 1
                        frame = 0


        # except:
        # # se c'è un errore durante l'applicazione stampa il tempo ed l'errore ed aspetta 1 secondo. 
        #    current_time = datetime.now().strftime("%H:%M:%S")
        #    print('💀'+Fore.RED+' errore '+  Style.RESET_ALL+' videocamera disconnessa alle ore : ',current_time)
        #    time.sleep(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python

# librerie built-in
import sys
import time
import socket
from datetime import datetime
from copy import deepcopy

# librerie di terze parti
import numpy as np
from colorama import Fore, Back, Style
import cv2
from PIL import Image
from matplotlib import cm
import depthai as dai

# file del progetto
import utils.systematik_opencv as sk
from utils.parametri import *
from utils.ricette import *
from utils.estetica import *

def aggiorna_parametri(val):
    '''
    aggiorna i parametri di visualizzazione presi dalla trackbar
    '''
    alpha = val / 100
    beta = ( 1.0 - alpha )
    #new = sk.computer_vision_system(video_frame.getCvFrame())
    #cv2.imshow('title', new)


def empty(a):
    pass


if __name__ == "__main__":
    # stampa logo, descrizione ed introduzione
    print(Fore.CYAN + LOGO + Style.RESET_ALL + '\n'+ descrizione )
    print('\n🚀 Computer Vision App '+ Fore.GREEN  +'[start]' + Style.RESET_ALL)
    
    # TCP socket server basato su IPv4 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa l'indirizzo IP e il numero di porta
    s.bind((IP_SERVER, PORTA_SERVER))

    # il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)
    s.listen(PORTA_SERVER)

    # accetta connessioni da uno specifico indirizzo
    connection , plc_address = s.accept()
    print(f"🛰️  connesso con macchina PLC con IP :  " + Fore.YELLOW + plc_address[0] + ':' + str(plc_address[1]) + Style.RESET_ALL )

    # inizializza videocamera di OpenKit con i seguenti parametri
    pipeline = dai.Pipeline()
    controllo = dai.CameraControl()
    camRgb = pipeline.createColorCamera()
    xoutVideo = pipeline.createXLinkOut()
    controlIn = pipeline.createXLinkIn()
    xoutVideo.setStreamName(nome_pannello_di_visualizzazione)
    controlIn.setStreamName('control')
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
    camRgb.setFps(float(FPS_frame))
    controllo.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
    camRgb.setVideoSize(video_size_x, video_size_y)
    controllo.setManualExposure(expTime,sensIso)
    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)
    camRgb.video.link(xoutVideo.input)

    while True:
        try:
            # configurazione videocamera Luxonis - Open AI kit (OAK) con libreria depthai
            with dai.Device(pipeline) as device:

                # crea interfaccia per visualizzare i risultati
                cv2.namedWindow(nome_pannello_di_visualizzazione)
                cv2.resizeWindow(nome_pannello_di_visualizzazione, video_size_x, video_size_y)

                # crea panello di controllo
                cv2.namedWindow(nome_pannello_di_controllo)
                cv2.resizeWindow(nome_pannello_di_controllo, video_size_x, video_size_y)

                # ottieni i valori delle trackbar dal pannello di controllo
                cv2.createTrackbar("FPS", nome_pannello_di_controllo, 0, 20, empty)
                cv2.createTrackbar("exposition", nome_pannello_di_controllo, 0, 55000, empty)
                cv2.createTrackbar("ISO", nome_pannello_di_controllo, 0, 500, empty)
                cv2.createTrackbar("focus", nome_pannello_di_controllo, 0, 1000, empty)
                cv2.createTrackbar("canny_x", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("canny_y", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("cartoon_x", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("cartoon_y", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("cartoon_z", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("line_x", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("line_y", nome_pannello_di_controllo, 0, 255, empty)
                cv2.createTrackbar("line_z", nome_pannello_di_controllo, 0, 255, empty)

                print('📷 videocamera '+ Fore.GREEN + '[online]' + Style.RESET_ALL)
                
                # inizializza videocamera
                video = device.getOutputQueue(name=nome_pannello_di_visualizzazione, maxSize=1, blocking=False)
                controlQueue = device.getInputQueue('control')
                ctrl = dai.CameraControl()
                ctrl.setManualExposure(expTime, sensIso)
                ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
                controlQueue.send(ctrl)

                while True: # all'infinito

                    # ricevi dati dal PLC tramite socket
                    data = connection.recv(1024)  

                    # try:
                        # Filtro per la PLC, se i dati contengono come primo carattere 'f' fai una foto
                        #if 'f' in str(data)[2]: 
                        #   print('📡 dati ricevuti da PLC: ' + Fore.BLUE  + str(data)  + Style.RESET_ALL + '\n taking photo ...')

                    # ottieni un immagine dalla videocamera
                    video_frame = video.get()

                    # ottieni i valori 
                    fps_value = cv2.getTrackbarPos("FPS", nome_pannello_di_controllo)
                    exposition_value = cv2.getTrackbarPos("exposition", nome_pannello_di_controllo)
                    ISO_value = cv2.getTrackbarPos("ISO", nome_pannello_di_controllo)
                    focus_value = cv2.getTrackbarPos("focus", nome_pannello_di_controllo)
                    canny_x_value = cv2.getTrackbarPos("canny_x", nome_pannello_di_controllo)
                    canny_y_value = cv2.getTrackbarPos("canny_y", nome_pannello_di_controllo)
                    line_x_value = cv2.getTrackbarPos("line_x", nome_pannello_di_controllo)
                    line_y_value = cv2.getTrackbarPos("line_y", nome_pannello_di_controllo)
                    line_z_value = cv2.getTrackbarPos("line_z", nome_pannello_di_controllo)
                    cartoon_x_value = cv2.getTrackbarPos("cartoon_x", nome_pannello_di_controllo)
                    cartoon_y_value = cv2.getTrackbarPos("cartoon_y", nome_pannello_di_controllo)
                    cartoon_z_value = cv2.getTrackbarPos("cartoon_z", nome_pannello_di_controllo)

                    # Computer Vision System
                    videoIn = sk.computer_vision_system(video_frame.getCvFrame())

                    # visualizza l'immagine nel pannello di visualizzazione
                    cv2.imshow(nome_pannello_di_visualizzazione, videoIn )    
                    
                    # visualizza immagine con parametri modificati
                    # on_trackbar(0)

                    # se premi C esci dall'applicazione
                    if cv2.waitKey(2) == ord('c'):
                        break
                    
                    print('📷 '+ Fore.YELLOW + '[photo]' + Style.RESET_ALL)
                    # salva immagine
                    # cv2.imwrite( path_salva_immagini  + '/t_' + counter + '.png',videoIn)

        # se c'è un errore durante l'applicazione stampa il tempo ed l'errore ed aspetta 1 secondo. 
        except:
            current_time = datetime.now().strftime("%H:%M:%S")
            print('💀 videocamera non rilevata '+ Fore.RED+'[disconnessa]'+Style.RESET_ALL+' alle ore',current_time)
            time.sleep(1)
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
import utils.systematik_opencv as systematik
from utils.params_network import PORTA_SERVER, IP_SERVER, IP_PLC, PORTA_PLC
from utils.ricette import ricetta_default
from utils.estetica import LOGO, descrizione, nome_pannello_di_controllo, nome_pannello_di_visualizzazione

def empty(a):
    pass


def main():
    '''
    Applicazione di Computer Vision
    1. inizializza il server
    2. aspetta il messaggio da client plc con socket con ID ricetta e ID pezzo
    3. scatta una foto e salvala
    4. elabora la foto rilevando i difetti
    5. ritorna la foto elaborata in una cartella
    6. ritorna lo status (presenza di errori) e l'ID del pezzo
    '''

    ricetta = {} # parametri per scattare la foto ed elaborarla
     
    fps = ricetta_default['fps']                
    video_size_x = ricetta_default['video_size_x']                
    video_size_y = ricetta_default['video_size_y']                
    manual_focus_parameter = ricetta_default['manual_focus_parameter']                
    exposition = ricetta_default['exposition']                
    iso = ricetta_default['iso']                
    canny_x = ricetta_default['canny_x']                
    canny_y = ricetta_default['canny_y']                
    line_x = ricetta_default['line_x']                
    line_y = ricetta_default['line_y']                
    line_z = ricetta_default['line_z']                
    cartoonize_x = ricetta_default['cartoonize_x']                
    cartoonize_y = ricetta_default['cartoonize_y']                
    cartoonize_z = ricetta_default['cartoonize_z']                
    min_canny_a = ricetta_default['min_canny_a']                
    max_canny_a = ricetta_default['max_canny_a']     
    min_canny_b = ricetta_default['min_canny_b']     
    max_canny_b = ricetta_default['max_canny_b']      

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
    camRgb.setFps(float(fps))
    controllo.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
    camRgb.setVideoSize(video_size_x, video_size_y)
    controllo.setManualExposure(exposition, iso)
    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)
    camRgb.video.link(xoutVideo.input)

    contatore_foto = 0

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
                cv2.createTrackbar("fps", nome_pannello_di_controllo, 0, 20, empty)
                cv2.createTrackbar("exposition", nome_pannello_di_controllo, 0, 55000, empty)
                cv2.createTrackbar("iso", nome_pannello_di_controllo, 0, 500, empty)
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
                ctrl.setManualExposure(exposition, iso)
                ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
                controlQueue.send(ctrl)

                while True: # all'infinito

                    # ricevi dati dal PLC tramite socket
                    data = connection.recv(1024)  

                    # fare attivare da qua sotto lo script
                    # filtro per la PLC, se i dati contengono come primo carattere 'f' fai una foto
                    if 'f' in str(data)[2]: 
                        print('📡 dati ricevuti da PLC: ' + Fore.BLUE  + str(data)  + Style.RESET_ALL + '\n taking photo ...')

                    try:
                        # ottieni un immagine dalla videocamera
                        video_frame = video.get()

                    except:
                        print('💀'+Fore.RED+' [errore]'+  Style.RESET_ALL+' | impossibile ottenere il frame dalla videocamera')

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


                    ##################################################################################
                    # 🤖 ｃｏｍｐｕｔｅｒ   ｖｉｓｉｏｎ
                    # i parametri modificati nel pannello di controllo con le trackbar vengono aggiornati ogni frame

                    frame = video_frame.getCvFrame()

                    frame_elaborato = systematik.computer_vision_system(frame, params=ricetta)
                    
                    cv2.imshow(nome_pannello_di_visualizzazione, frame_elaborato)

                    print('📷 esecuzione frame '+ Fore.GREEN + '[photo]' + Style.RESET_ALL)
                    ##################################################################################

                    # se premi C esci dall'applicazione
                    if cv2.waitKey(2) == ord('c'):
                        break
                    
                    # se premi S salvi una foto
                    if cv2.waitKey(1) & 0xFF == ord('s'): 
                        cv2.imwrite(sys.path[0]+"/data/img/viz/foto_"+str(contatore_foto)+".png",frame)
                        contatore_foto += 1
                        time.sleep(0.1)
                                       
                    # salva immagine
                    # cv2.imwrite( path_salva_immagini  + '/t_' + counter + '.png',video_frame)

        # se c'è un errore durante l'applicazione stampa il tempo ed l'errore ed aspetta 1 secondo. 
        except:
            current_time = datetime.now().strftime("%H:%M:%S")
            print('💀'+Fore.RED+' [errore]'+  Style.RESET_ALL+'| videocamera disconnessa alle ore: ',current_time)
            time.sleep(1)

if __name__ == "__main__":
    main()

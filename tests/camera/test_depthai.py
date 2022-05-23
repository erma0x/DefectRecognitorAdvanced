import sys
import argparse
from datetime import datetime
from time import sleep
import cv2
import depthai as dai


# LANCIARE LO SCRIPT
# python3  .\tests\camera\depthai_test.py "14442C1001293DD700" "viz"


########## parametri ################################################################
# parametri per la videocamera di depthaAI
nome_pannello_di_controllo = "video"
FPS_frame = 5                                  # fps frame per second : intervallo fra 1-120 
manual_focus_parameter = 100                    # focus manuale : intervallo fra 0-255 
expTime = 33000                                 # tempo di esposizione in milliseconds : intervallo fra 1-100_000
sensIso = 100                                   # sensibilità del sensore della fotocamera : intervallo fra 0-500
video_size_x = 1000                             # grandezza video asse X in pixels
video_size_y = 700                              # grandezza video asse Y in pixels

#####################################################################################

parser = argparse.ArgumentParser()

parser.add_argument('id_camera', type=str)  # ID modello videocamera OAK passato da linea di comando
parser.add_argument('tipo_camera', type=str)     # nome cartella img in cui salvare le foto
parser.add_argument('intervallo_secondi', type=int)     

args = parser.parse_args()

ID_CAMERA = args.id_camera
TIPO_CAMERA = args.tipo_camera

INTERVALLO_SECONDI = 10
INTERVALLO_SECONDI = args.intervallo_secondi



######### inizializzazione ##############################################################

# inizializza la videocamera con depthai
pipeline = dai.Pipeline()
controllo = dai.CameraControl()
camRgb = pipeline.createColorCamera()
xoutVideo = pipeline.createXLinkOut()
controlIn = pipeline.createXLinkIn()
xoutVideo.setStreamName(nome_pannello_di_controllo)
controlIn.setStreamName('control')
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)

# setta la risoluzione della vidocamera 
# modalità disponibili sono: 4k, 1080p, 12mega pixel (THE_4_K,THE_1080_P, THE_12_MP )
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)        # 4K

# setta i frame per secondo
camRgb.setFps(float(FPS_frame))



######### focus control #########################################################################
# setta la modalità per il focus automatico
# modalita' di focus: AUTO, MACRO, CONTINUOUS_VIDEO, CONTINUOUS_PICTURE, OFF, EDOF
controllo.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)

# setta il focus in manuale usare il seguente comando
controllo.setManualFocus(manual_focus_parameter)

# setta la regione da zoommare e gestire con l'autofocus
#controllo.setAutoFocusRegion(dai.CameraControl,int(1670),int(770),int(660),int(500))


# setta la grandezza video con le coordinate X & Y in pixels
camRgb.setVideoSize(video_size_x, video_size_y)

# modalità disponibili: ACTION, STEADYPHOTO
#controllo.setSceneMode(dai.CameraControl.SceneMode.ACTION)

# setta il tempo di esposizione manuale 
#controllo.setManualExposure(expTime,sensIso)
#controlQueue.send(controllo)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)
camRgb.video.link(xoutVideo.input)

found, device_info = dai.Device.getDeviceByMxId(ID_CAMERA)

if not found:
    raise RuntimeError("Videocamera non trovata! Perfavore riprova")

######### start process #############################################################################

i=0

while True:
    with dai.Device(pipeline, device_info) as device:
        video = device.getOutputQueue(name=nome_pannello_di_controllo, maxSize=1, blocking=False)
        controlQueue = device.getInputQueue('control')
        ctrl = dai.CameraControl()
        ctrl.setManualExposure(expTime, sensIso)
        ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
        controlQueue.send(ctrl)  
    
        while True:
        
            videoIn = video.get()
            cv2.namedWindow(nome_pannello_di_controllo, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(nome_pannello_di_controllo, video_size_x, video_size_y)
            frame =  videoIn.getCvFrame()
            cv2.imshow(nome_pannello_di_controllo, frame)
            
            i+=1
            sleep(int(INTERVALLO_SECONDI))
            cv2.imwrite(sys.path[0]+"/img/"+str(TIPO_CAMERA)+"/foto_"+str(i)+".png",frame) 

            if cv2.waitKey(2) == ord('c'):
                break
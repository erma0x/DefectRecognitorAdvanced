from datetime import datetime
import cv2
import depthai as dai
import sys


########## parametri ################################################################

# parametri per la videocamera di depthaAI
nome_pannello_di_controllo = "video"
FPS_frame = 10                                  # fps frame per second : intervallo fra 1-120 
manual_focus_parameter = 100                    # focus manuale : intervallo fra 0-255 
expTime = 33000                                 # tempo di esposizione in milliseconds : intervallo fra 1-100_000
sensIso = 100                                   # sensibilità del sensore della fotocamera : intervallo fra 0-500
video_size_x = 1000                             # grandezza video asse X in pixels
video_size_y = 700                              # grandezza video asse Y in pixels




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
#controllo.setManualFocus(manual_focus_parameter)

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


######### start process #############################################################################

while True:
    try:
        with dai.Device(pipeline) as device:
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

                # se premi il tasto C salvi una foto
                if cv2.waitKey(1) & 0xFF == ord('s'): #save on pressing 'y' 
                    cv2.imwrite(sys.path[0]+"/foto_"+str(i)+".png",frame) 
                    i=i+1
                    
                if cv2.waitKey(2) == ord('c'):
                    break
    except:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('camera disconnessa alle ore ',current_time)
from datetime import datetime
import cv2
import depthai as dai

nome_pannello_di_controllo = "video"
FPS_frame = 10 # intervallo fra 0-120 
manual_focus_parameter = 100  # focus manuale: intervallo fra 0-255 
expTime = 33000
sensIso = 100
video_size_x = 1000
video_size_y = 700



pipeline = dai.Pipeline()
controllo = dai.CameraControl()

camRgb = pipeline.createColorCamera()
xoutVideo = pipeline.createXLinkOut()
controlIn = pipeline.createXLinkIn()
xoutVideo.setStreamName(nome_pannello_di_controllo)
controlIn.setStreamName('control')
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)

camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)        # 4K
#camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)    # 1080 P 
#camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)     # 12 MP

camRgb.setFps(float(FPS_frame))

controllo.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
# modalita' di focus: AUTO, MACRO, CONTINUOUS_VIDEO, CONTINUOUS_PICTURE, OFF, EDOF

#controllo.setManualFocus(manual_focus_parameter)

camRgb.setVideoSize(video_size_x, video_size_y)

#controllo.setSceneMode(dai.CameraControl.SceneMode.ACTION)# MODALITA': STEADYPHOTO,ACTION
#controllo.setAutoFocusRegion(dai.CameraControl,int(1670),int(770),int(660),int(500))

#controllo.setManualExposure(expTime,sensIso) # tempo di esposizione
#controlQueue.send(controllo)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)
camRgb.video.link(xoutVideo.input)

#fps.print_status()
#print(camRgb.getFps())

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
                cv2.imshow(nome_pannello_di_controllo, videoIn.getCvFrame())


                if cv2.waitKey(2) == ord('c'):
                    break
    except:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('camera disconnessa alle ore ',current_time)
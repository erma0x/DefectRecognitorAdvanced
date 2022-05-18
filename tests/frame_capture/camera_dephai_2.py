def start_camera():

    # configurazione videocamera Luxonis
    print('📷 videocamera '+ Fore.GREEN + '[start]' + Style.RESET_ALL)
    pipeline = dai.Pipeline()
    controllo = dai.CameraControl()
    camRgb = pipeline.createColorCamera()
    xoutVideo = pipeline.createXLinkOut()
    controlIn = pipeline.createXLinkIn()
    xoutVideo.setStreamName(nome_pannello_di_controllo)
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

    # 
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
            print('🌠 videocamera'+ Fore.RED+' [disconnessa]'+Style.RESET_ALL+' alle ore ',current_time)
            time.sleep(2)
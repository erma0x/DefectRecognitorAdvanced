import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


torch.save(model, "/home/kobayashi/Documents/object-detection-opencv/model_yolov5s.h5")

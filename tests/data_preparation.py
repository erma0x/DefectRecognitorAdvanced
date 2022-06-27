import pandas as pd
import numpy as np
import cv2

labels = pd.read_csv("/content/content/eye_gender_data/Training_set.csv") # loading the labels

file_paths = [[fname, "/content/content/eye_gender_data/train/" + fname] for fname in labels["filename"]]
images = pd.DataFrame(file_paths, columns=["filename", "filepaths"])
train_data = pd.merge(images, labels, how = "inner", on = "filename")

data = [] # initialize an empty numpy array
image_size = 100 # image size taken is 100 here. one can take other size too

for i in range(len(train_data)):
    img_array = cv2.imread(train_data["filepaths"][i], cv2.IMREAD_GRAYSCALE) # converting the image to gray scale
    new_img_array = cv2.resize(img_array, (image_size, image_size)) # resizing the image array
    data.append([new_img_array, train_data["label"][i]])
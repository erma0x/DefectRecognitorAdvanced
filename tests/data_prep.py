from PIL import Image
import os
import numpy as np
import re


''' objective
from image(.png/.jpeg) to np.array
'''

''' source
https://www.codespeedy.com/prepare-your-own-data-set-for-image-classification-python/
'''

import os
def resize_multiple_images(src_path, dst_path):
    # Here src_path is the location where images are saved.
    for filename in os.listdir(src_path):
        try:
            img=Image.open(src_path+filename)
            new_img = img.resize((64,64))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            new_img.save(dst_path+filename)
            print('Resized and saved {} successfully.'.format(filename))
        except:
            continue

src_path = <Enter the source path>
dst_path = <Enter the destination path>
resize_multiple_images(src_path, dst_path)




def rename_multiple_files(path,obj):

    i=0

    for filename in os.listdir(path):
        try:
            f,extension = os.path.splitext(path+filename)
            src=path+filename
            dst=path+obj+str(i)+extension
            os.rename(src,dst)
            i+=1
            print('Rename successful.')
        except:
            i+=1

path=<Enter the path of objects to be renamed>
obj=<Enter the prefix to be added to each file. For ex. car, bike, cat, dog, etc.>
rename_multiple_files(path,obj)


def get_data(path):
    all_images_as_array=[]
    label=[]
    for filename in os.listdir(path):
        try:
            if re.match(r'car',filename):
                label.append(1)
            else:
                label.append(0)
            img=Image.open(path + filename)
            np_array = np.asarray(img)
            l,b,c = np_array.shape
            np_array = np_array.reshape(l*b*c,)
            all_images_as_array.append(np_array)
        except:
            continue

    return np.array(all_images_as_array), np.array(label)

path_to_train_set = <Enter the location of train set>
path_to_test_set = <Enter the location of test set>
X_train,y_train = get_data(path_to_train_set)
X_test, y_test = get_data(path_to_test_set)

print('X_train set : ',X_train)
print('y_train set : ',y_train)
print('X_test set : ',X_test)
print('y_test set : ',y_test)

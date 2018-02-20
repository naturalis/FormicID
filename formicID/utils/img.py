################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                    Utilities                                 #
#                                 Image handeling                              #
################################################################################
'''
Description:
<placeholder txt>
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////
import os

import cv2

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
wd = os.getcwd()

# Load and show images
# //////////////////////////////////////////////////////////////////////////////

def load_img(image):
    img_path = os.path.join(wd, path, img)
    img = img.read('image', img_path
    return img

def show_img(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Visualizing data agumentation
################################################################################
# TODO (MJABOER):
# import ImageDataGenerator from test data_input.py
# this is a PIL image
img = load_img('data/train/lasiusflavus/lasiusflavus1.jpg')

# this is a Numpy array with shape (3, 150, 150)
x = img_to_array(img)

# this is a Numpy array with shape (1, 3, 150, 150)
x = x.reshape((1,) + x.shape)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='preview',
                          save_prefix='lasiusflavus',
                          save_format='jpeg'):
    i += 1
    if i > 20:
        break  # otherwise the generator would loop indefinitely

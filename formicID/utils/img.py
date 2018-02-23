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
'''Description:
This script contains several image related scripts that can be loaded in to
other files.
'''
# Packages
################################################################################
import os

from keras.preprocessing.image import img_to_array, load_img

import cv2
from trainers.train import train_data_generator

# Parameters and settings
################################################################################
wd = os.getcwd()

# Load and show images
################################################################################


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
def show_augment(image, input_dir):
    # TODO (MJABOER):
    # import ImageDataGenerator from test data_input.py
    # import create_dirs()

    img_file=os.path.jon(wd, input_dir, image)

    # this is a PIL image
    img_loaded=load_img(img_file)

    # this is a Numpy array with shape (3, 150, 150)
    img=img_to_array(img_loaded)

    # this is a Numpy array with shape (1, 3, 150, 150)
    img=x.reshape((1,) + x.shape)

    # the .flow() command below generates batches of randomly transformed images
    # and saves the results to the `preview/` directory
    i=0
    for batch in train_data_generator.flow(x,
                                           batch_size=1,
                                           save_to_dir='preview',
                                           save_prefix='lasiusflavus',
                                           save_format='jpeg'):
        i += 1
        if i > 20:
            break  # otherwise the generator would loop indefinitely

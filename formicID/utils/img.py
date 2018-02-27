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

# import matplotlib.pyplot as plt
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import (ImageDataGenerator, img_to_array,
                                       load_img)

from trainers.train import train_data_generator

from .utils import wd

# Parameters and settings
################################################################################


# Load and show images
################################################################################


# def load_img(path, img):
#     img_path = os.path.join(wd, path, img)
#     img = img.read('image', img_path)
#     return img


# def show_img(image):
    # implement keras show img


# Visualizing data agumentation
################################################################################


def save_augmentation(image, test_dir, input_dir):
    """This function returns 20 random augmented versions of an input image.

    Args:
        image (str): image name.
        test_dir (str): directory that contains the `images` folder
        input_dir (str): path inside test_dir that leads to the image.

    Returns:
        type: 20 augmented images of the input image

    """
    # TODO (MJABOER):
    # import ImageDataGenerator from test data_input.py
    # import create_dirs()

    if not os.path.exists(os.path.join(wd, test_dir, 'images', 'augment')):
        os.mkdir(os.path.join(wd, test_dir, 'images', 'augment'))

    output_dir=os.path.join(wd, test_dir, 'images', 'augment')
    input_dir=os.path.join(wd, test_dir, input_dir)
    filename=image.replace('.jpeg', '')

    img_file=os.path.join(wd, input_dir, image)
    img_loaded=load_img(img_file)
    img=img_to_array(img_loaded)
    img=img.reshape((1,) + img.shape)

    i=0
    train_data_gen = ImageDataGenerator(
        preprocessing_function=preprocess_input, # needed for inception_v3
        # rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    for batch in train_data_gen.flow(img,
                                     batch_size=1,
                                     save_to_dir=output_dir,
                                     save_prefix=filename,
                                     save_format='jpeg'):
        i += 1
        if i > 20:
            break

    print('Augmented files can be found in {}'.format(output_dir))


# def plot_figs(num_species, images, labels):
#
#     fig = plt.figure(figsize=(8,3))
#     i = 0
#     for i in range(num_species):
#         ax = fig.add_subplot(2,3,1 + i, xticks=[], yticks=[])
#         features_idx = images[labels[:]==i,:]
#         ax.set_title(str(i))
#         plt.imshow(features_idx[1], cmap='gray')
#         i + 1
#     plt.show()

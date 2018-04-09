###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                    Utilities                                #
#                                 Image handeling                             #
###############################################################################
'''Description:
This script contains several image related scripts that can be loaded in to
other files.
'''
# Packages
###############################################################################

# Standard library imports
import logging
import os
from math import ceil

# Deeplearning tools imports
from keras.preprocessing.image import array_to_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.utils.np_utils import to_categorical

# Data tools imports
import numpy as np

# Graphical tools imports
import matplotlib.pyplot as plt

# Additional project imports
import PIL  # Imports PIL-SIMD. PIL is needed for load_img()

# FormicID imports
from trainers.train import idg
from .utils import wd

# Parameters and settings
###############################################################################


# Load and show images
###############################################################################

def show_img(
    array
):
    image = array_to_img(array)
    plt.imshow(image)
    plt.show()


def show_multi_img(
    X_train,
    Y_train,
    cols=4,
    rows=4
):
    """Plot n images of X_train using matplotlib.

    Args:
        X_train (array): Images, represented as a 4D array.
        Y_train (array): Labels of the images .
        cols (int): Number of images per column. Defaults to 4.
        rows (int): Number of images per row. Defaults to 4.

    Returns:
        image: a plot of cols * rows images.

    """
    images = cols * rows
    fig = plt.figure(figsize=(8, 8))
    for i in range(1, images + 1):
        img = array_to_img(X_train[i])
        label = np.argmax(Y_train[i], axis=0, out=None)
        fig.add_subplot(rows, cols, i, xticks=[], yticks=[])
        plt.title(label)
        plt.imshow(img)
    plt.show()

# Visualizing data agumentation
###############################################################################


def save_augmentation(
    image,
    config
):
    """This function returns 20 random augmented versions of an input image.

    Args:
        image (str): path to image.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        files: 20 augmented images (`.jpeg`) of the input image inside the
        experiment folder.

    """
    if not os.path.exists(os.path.join(config.summary_dir, 'augmented')):
        os.mkdir(os.path.join(config.summary_dir, 'augmented'))
    augment_dir = os.path.join(config.summary_dir, 'augmented')
    filename, _ = os.path.split(image)
    filename = os.path.basename(filename)
    img_loaded = load_img(image)
    img = img_to_array(img_loaded)
    img = img.reshape((1,) + img.shape)
    i = 0
    idgen = idg(target_gen='training')
    for batch in idgen.flow(
        img,
        batch_size=1,
        save_to_dir=augment_dir,
        save_prefix=filename,
        save_format='jpeg'
    ):
        i += 1
        if i > 19:
            break
    logging.info('Augmented files can be found in {}'.format(augment_dir))


def show_augmentation_from_dir(
    aug_dir,
    max_img,
    n_cols=4
):
    """Short summary.

    Args:
        aug_dir (type): Description of parameter `aug_dir`.
        max_img (type): Description of parameter `max_img`.
        n_cols (type): Description of parameter `n_cols`. Defaults to 4.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    img_list = os.listdir(aug_dir)
    fig = plt.figure(figsize=(8, 8))
    n_rows = int(ceil(max_img // n_cols))
    i = 1
    for img in img_list[0:max_img]:
        image = load_img(path=os.path.join(aug_dir, img))
        fig.add_subplot(n_rows, n_cols, i)
        plt.imshow(image)
        i += 1
    plt.show()

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
"""Description:
This script contains several image related scripts that can be loaded in to
other files.
"""

# Packages
###############################################################################

# Standard library imports
import logging
import os
import random
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
import PIL  # Imports PIL-SIMD. PIL is needed for load_img()

# FormicID imports
from trainers.train import idg

# Visualizing data agumentation
###############################################################################


def _show_augmentation_from_dir(aug_dir, max_img, n_cols=4):
    """Visualize a number of augmented images from a directory.

    Args:
        aug_dir (str): Path to directory that holds the augmented images.
        max_img (int): Maximum number of images as subplot in the plot.
        n_cols (int): Number of columns to divide the images in.
            Automatically calculates the number of rows to complement to the
            maximum number of images. Defaults to 4.

    """
    # TODO: Test the no tickmarks line
    img_list = os.listdir(aug_dir)
    fig = plt.figure(figsize=(8, 8))
    n_rows = int(ceil(max_img // n_cols))
    max_div = n_cols * n_rows

    i = 1
    plt.tight_layout()
    axes = [fig.add_subplot(n_rows, n_cols, i) for i in range(1, max_div + 1)]
    plt.setp(axes, xticks=[], yticks=[])
    for img in img_list[0:max_img]:
        image = load_img(path=os.path.join(aug_dir, img))
        fig.add_subplot(n_rows, n_cols, i)
        plt.imshow(image)
        i += 1
    plt.tight_layout()
    plt.show()


def save_augmentation(image, config, show=False):
    """This function saves 20 random augmented (jpg) image versions of an
    input image to a directory.

    Args:
        image (str): path to image.
        config (Bunch object): The JSON configuration Bunch object.
        show (Bool): Wheter to show the augmentation after saving or not. Defaults to False.

    """
    if not os.path.exists(os.path.join(config.summary_dir, "augmented")):
        os.mkdir(os.path.join(config.summary_dir, "augmented"))
    augment_dir = os.path.join(config.summary_dir, "augmented")
    filename, _ = os.path.split(image)
    filename = os.path.basename(filename)
    img_loaded = load_img(image)
    img = img_to_array(img_loaded)
    img = img.reshape((1,) + img.shape)
    i = 0
    idgen = idg(config=config, target_gen="training")
    for batch in idgen.flow(
        img,
        batch_size=1,
        save_to_dir=augment_dir,
        save_prefix=filename,
        save_format="jpeg",
    ):
        i += 1
        if i > 19:
            break

    logging.info("Augmented files can be found in {}".format(augment_dir))
    if show:
        _show_augmentation_from_dir(aug_dir=augment_dir, max_img=20, n_cols=5)


def show_dataset(
    image_dir, config, max_img, n_cols=4, save=None, transparent=True
):
    seed = config.seed
    exts = [".jpg", ".jpeg", ".png"]
    img_list = []
    for root, subdirs, files in os.walk(image_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in exts:
                img_list.append(os.path.join(root, file))
    random.shuffle(img_list)
    img_list = img_list[:max_img]
    n_rows = int(ceil(max_img // n_cols))
    fig = plt.figure(figsize=(8, 8))
    plt.tight_layout()
    max_div = n_cols * n_rows
    axes = [fig.add_subplot(n_rows, n_cols, i) for i in range(1, max_div + 1)]
    plt.setp(axes, xticks=[], yticks=[])
    for img, ax in zip(img_list, axes):
        _, title = os.path.split(img)
        title, _ = os.path.splitext(title)
        img_plot = load_img(img)
        ax.imshow(img_plot)
        ax.set_title(title, size=7)
    plt.tight_layout()
    plt.show()
    if save is not None:
        plt.savefig(save, transparent=transparent)

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
import os

# import matplotlib.pyplot as plt
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img

from trainers.train import idg_train

from .utils import wd

# Parameters and settings
###############################################################################


# Load and show images
###############################################################################


def load_image(img):
    img = load_img(img)
    return img


def show_img(image):
    raise NotImplementedError


def show_multi_img(num_species, images, labels):

    fig = plt.figure(figsize=(8,3))
    i = 0
    for i in range(num_species):
        ax = fig.add_subplot(2,3,1 + i, xticks=[], yticks=[])
        features_idx = images[labels[:]==i,:]
        ax.set_title(str(i))
        plt.imshow(features_idx[1], cmap='gray')
        i + 1
    plt.show()

# Visualizing data agumentation
###############################################################################


def save_augmentation(image, config):
    """This function returns 20 random augmented versions of an input image.

    Args:
        image (str): path to image.
        config (str): configuration file

    Returns:
        type: 20 augmented images of the input image inside the experiment
        folder.

    """
    if not os.path.exists(os.path.join(config.summary_dir, 'augmented')):
        os.mkdir(os.path.join(config.summary_dir, 'augmented'))

    augment_dir = os.path.join(config.summary_dir, 'augmented')

    filename, _ = os.path.split(image)
    filename = os.path.basename(filename)

    img_file = image

    img_loaded = load_img(img_file)
    img = img_to_array(img_loaded)
    img = img.reshape((1,) + img.shape)

    i = 0
    idgen_train = idg_train()
    for batch in idgen_train.flow(img,
                                batch_size=1,
                                save_to_dir=augment_dir,
                                save_prefix=filename,
                                save_format='jpeg'):
        i += 1
        if i > 19:
            break

    print('Augmented files can be found in {}'.format(augment_dir))

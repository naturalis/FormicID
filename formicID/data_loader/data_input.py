################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  data_input                                  #
################################################################################
'''
Description:
<placeholder txt>

    The directory structure:
    directory_name/
        head/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...
        dorsal/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...

'''
# Packages
################################################################################
import os

import numpy as np
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.utils import normalize
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder

import cv2
from tqdm import tqdm

# Parameters and settings
################################################################################
wd = os.getcwd()
seed = 1337
img_width, img_height = 85, 85

# Load images
################################################################################


def img_load_shottype(shottype, datadir):
    """Short summary.

    Args:
        shottype (type): Description of parameter `shottype`.
        datadir (type): Description of parameter `datadir`.

    Returns:
        type: Description of returned object.
    """
    # TODO (MJABOER):
    # Normalize image data (see datagenerators)

    data_dir = os.path.join(wd, 'data', datadir, 'images')
    if shottype == 'h':
        data_dir = os.path.join(data_dir, 'head')
    if shottype == 'd':
        data_dir = os.path.join(data_dir, 'dorsal')
    if shottype == 'p':
        data_dir = os.path.join(data_dir, 'profile')

    images = []
    labels = []
    print('Reading images from "{}"'.format(data_dir))
    for species in tqdm(os.listdir(data_dir),
                        desc='Reading folders',
                        unit='species'):
        for image in tqdm(os.listdir(os.path.join(data_dir, species)),
                          desc='Loading {}'.format(species),
                          unit='images'):
            if '.jpg' in image:
                img = cv2.imread(os.path.join(data_dir, species, image))
                img = cv2.resize(img,
                                (img_width, img_height),
                                interpolation=cv2.INTER_AREA)
                img = np.asarray(img)
                # returns BGR instead of RGB
                if img is not None:
                    # img = img[:, :, ::-1]  # Convert to RGB
                    images = np.append(images, img)
            label = species
            labels = np.append(labels, label)
    print('\n') # to correctly print tqdm when finished.
    images = np.reshape(images, (-1, img_width, img_height, 3))
    # Cast np array to keras default float type ('float32')
    images = K.cast_to_floatx(images)
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    # divide by 2, because of the recursive call to data_dir
    labels = to_categorical(labels, num_classes=len(species)//2)
    labels = K.cast_to_floatx(labels)

    # print('after', labels)
    # print('\nImages shape: ',images.shape)
    # print('images dtype: ', images.dtype)
    # print('labels shape: ', labels.shape)
    # print('labels dtype: ', labels.dtype)

    return images, labels


# Training, validation and test split
################################################################################


def train_val_test_split(images, labels, test_size, val_size):
    """Short summary.

    Args:
        images (type): Description of parameter `images`.
        labels (type): Description of parameter `labels`.
        test_size (type): Description of parameter `test_size`.
        val_size (type): Description of parameter `val_size`.

    Returns:
        type: Description of returned object.
    """
    sss = StratifiedShuffleSplit(
        n_splits=1, test_size=test_size, random_state=seed)
    sss.get_n_splits(images, labels)
    # print(sss)
    for train_index, test_index in sss.split(images, labels):
        print('TEST (10%%): {}'.format(test_index))
        X_train, X_test = images[train_index], images[test_index]
        Y_train, Y_test = labels[train_index], labels[test_index]

        sss = StratifiedShuffleSplit(
            n_splits=1, test_size=val_size, random_state=seed)
        sss.get_n_splits(X_train, Y_train)
        # print(sss)
        for train_index, val_index in sss.split(X_train, Y_train):
            # print('\nTRAIN (~75%%): {} \n\nVAL (~15%%): {}'.format(
            #     train_index, val_index))
            X_train, X_val = X_train[train_index], X_train[val_index]
            Y_train, Y_val = Y_train[train_index], Y_train[val_index]

        nb_specimens = len(X_test) + len(X_train) + len(X_val)
        print('Number of X_test: {}'.format(len(X_test)))
        print('Number of X_train: {}'.format(len(X_train)))
        print('Number of X_val: {}'.format(len(X_val)))
        print('Number of labels: {}'.format(nb_specimens))

        return X_train, Y_train, X_val, Y_val, X_test, Y_test

# Train data generator
################################################################################
def train_data_generator(X_train, Y_train, batch_size, epochs):
    """Short summary.

    Args:
        X_train (type): Description of parameter `X_train`.
        Y_train (type): Description of parameter `Y_train`.
        batch_size (type): Description of parameter `batch_size`.
        epochs (type): Description of parameter `epochs`.

    Returns:
        type: Description of returned object.

    - rescale: Rescaling factor; normalizing the data to [0:1]
    - rotation_range: degree range for random rotations (integer)
    - width_shift_range: range for random horizontal shifts (float)
    - height_shift_range: range for random vertical shifts (float)
    - shear_range: shear intensity (float)
    - zoom_range: range for random zoom (float)
    - horizontal_flip: randomly flip inputs horizontally (boolean)
    """
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    # TODO (MJABOER):
        # ImageDataGenerator.standardize
    train_generator = train_datagen.flow(X_train, Y_train, seed=seed)
    return train_generator

# validation data generator
################################################################################
def val_data_generator(X_val, Y_val, batch_size, epochs):
    """Short summary.

    Args:
        X_val (type): Description of parameter `X_val`.
        Y_val (type): Description of parameter `Y_val`.
        batch_size (type): Description of parameter `batch_size`.
        epochs (type): Description of parameter `epochs`.

    Returns:
        type: Description of returned object.
    """
    # TODO (MJABOER):
        # ImageDataGenerator.standardize
    val_datagen = ImageDataGenerator(rescale=1. / 255)
    validation_generator = val_datagen.flow(X_val, Y_val, seed=seed)
    return validation_generator

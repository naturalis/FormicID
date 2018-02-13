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
from keras.utils import to_categorical # one-hot encoding
from keras.utils import normalize
from sklearn.model_selection import StratifiedShuffleSplit

import cv2

# from keras.preprocessing.image import ImageDataGenerator
# from keras.preprocessing.image import array_to_img, img_to_array, load_img

# Parameters and settings
################################################################################
wd = os.getcwd()

seed = 1337

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
    # convert labels to binary class matrix (utils.to_categorical)
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
    for species in os.listdir(data_dir):
        for image in os.listdir(os.path.join(data_dir, species)):
            if '.jpg' in image:
                img = cv2.imread(os.path.join(data_dir, species, image))
                # returns BGR instead of RGB
                if img is not None:
                    # img = img[:, :, ::-1]  # Convert to RGB
                    images.append(img)
            label = species
            labels.append(label)
    images = np.asarray(images)
    labels = np.asarray(labels)
    return images, labels


images, labels = img_load_shottype(shottype='h', datadir='2018-02-12-test')

type(images)
# Training, validation and test split
################################################################################


def train_val_test_split(images, labels, test_size, val_size):
    """Short summary.

    Args:
        images (type): Description of parameter `images`.
        labels (type): Description of parameter `labels`.
        test_size (type): Description of parameter `test_size`.
        random_state (type): Description of parameter `random_state`.

    Returns:
        type: Description of returned object.

    """
    nb_classes = len(set(labels))

    sss = StratifiedShuffleSplit(
        n_splits=1, test_size=test_size, random_state=seed)
    sss.get_n_splits(images, labels)
    # print(sss)
    for train_index, test_index in sss.split(images, labels):
        print('TEST (10%%): {}'.format(test_index))
        X_train, X_test = images[train_index], images[test_index]
        Y_train, Y_test = labels[train_index], labels[test_index]

        nb_classes = len(set(labels))
        sss = StratifiedShuffleSplit(
            n_splits=1, test_size=val_size, random_state=seed)
        sss.get_n_splits(X_train, Y_train)
        # print(sss)
        for train_index, val_index in sss.split(X_train, Y_train):
            print('\nTRAIN (~75%%): {} \n\nVAL (~15%%): {}'.format(
                train_index, val_index))
            X_train, X_val = X_train[train_index], X_train[val_index]
            Y_train, Y_val = Y_train[train_index], Y_train[val_index]

        print('Number of X_test: {}'.format(len(X_test)))
        print('Number of X_train: {}'.format(len(X_train)))
        print('Number of X_val: {}'.format(len(X_val)))
        print('Number of Y_train: {} with {} classes'.format(len(labels),
                                                             nb_classes))

        return X_train, Y_train, X_val, Y_val, X_test, Y_test


X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
    images=images, labels=labels, test_size=0.1, val_size=0.135)


# Train en test data augumentation
################################################################################


# Don't augment the testdata. Only rescale to normalize the data
validation_gen = ImageDataGenerator(
    rescale=1. / 255
)


# Train en validation datagenerators
################################################################################
def train_data_generator(X_train, Y_train, batch_size, epochs):
    """Short summary.

    Args:
        X_train (type): Description of parameter `X_train`.
        Y_train (type): Description of parameter `Y_train`.

    Returns:
        type: Description of returned object.

    rescale: Rescaling factor; normalizing the data to [0:1]
    rotation_range: degree range for random rotations (integer)
    width_shift_range: range for random horizontal shifts (float)
    height_shift_range: range for random vertical shifts (float)
    shear_range: shear intensity (float)
    zoom_range: range for random zoom (float)
    horizontal_flip: randomly flip inputs horizontally (boolean)
    """
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train_datagen.fit(X_train)

    train_generator = train_datagen.flow(
        X_train, Y_train, augment=False, rounds=1, seed=seed, batch_size=batch_size, steps_per_epoch-len(X_train) / batch_size, epochs = epochs)

    return train_generator


# def validation_data_generator(directory):
#     """
#     input = link to a folder containing a set of validation images
#
#     target_size resizes images to new dimensions
#     class_mode must be 'categorical' because of 2D data
#
#     # Don't set classes. It will take the classes from subdirectories.
#     # save_dir= 'dir' # can use to save the augmentated images
#     # also use (save_prefix, save_format) then
#
#     """
#     validation_generator = validation_gen.flow_from_directory(
#         directory,
#         target_size=(img_height, img_width),
#         batch_size=batch_size,
#         class_mode='categorical'
#     )
#     return validation_generator
#
#
# """
#
# Visualizing data agumentation
#
# # Data augmentation
# # //////////////////////////////////////////////////////////////////////////////
# datagen = ImageDataGenerator(
#     rotation_range=40,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest')
#
# # this is a PIL image
# img = load_img('data/train/lasiusflavus/lasiusflavus1.jpg')
#
# # this is a Numpy array with shape (3, 150, 150)
# x = img_to_array(img)
#
# # this is a Numpy array with shape (1, 3, 150, 150)
# x = x.reshape((1,) + x.shape)
#
# # the .flow() command below generates batches of randomly transformed images
# # and saves the results to the `preview/` directory
# i = 0
# for batch in datagen.flow(x, batch_size=1,
#                           save_to_dir='preview',
#                           save_prefix='lasiusflavus',
#                           save_format='jpeg'):
#     i += 1
#     if i > 20:
#         break  # otherwise the generator would loop indefinitely
# """

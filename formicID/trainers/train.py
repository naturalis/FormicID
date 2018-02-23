################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Trainer                                     #
#                                                                              #
################################################################################
'''
Description:
This file contains data generators. These generators generate batches of tensor
image data while also augmenting the images in real-time. The data will be
looped over (in batches) indefinitely. There is a train_data_generator, which
also augments the images with different methods, and a val_data_generator which
does only preprocess the data. Validation data should not be augmented. The
`preprocessing_function` is needed for the inception_v3 model.
'''

# Packages
################################################################################
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.inception_v3 import preprocess_input

# TODO (MJABOER):
# loop over batches while training. This is better for the memory.
# Add EarlyStopping

# Parameters and settings
################################################################################
seed = 1

# Training
################################################################################

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
        preprocessing_function=preprocess_input, # needed for inception_v3
        # rescale=1. / 255,
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
    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input, # needed for inception_v3
        # rescale=1. / 255)
    validation_generator = val_datagen.flow(X_val, Y_val, seed=seed)
    return validation_generator

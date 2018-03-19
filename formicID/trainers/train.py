###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Trainer                                    #
#                                                                             #
###############################################################################
'''
Description:
This file contains data generators. These generators generate batches of tensor
image data while also augmenting the images in real-time. The data will be
looped over (in batches) indefinitely. There is a train_data_generator, which
also augments the images with different methods, and a val_data_generator which
does only preprocess the data. Validation data should not be augmented. The
`preprocessing_function` is needed for the inception_v3 model. It scales the
pixels in  `[-1, 1]`, samplewise and using the following calculation:
    `x /= 127.5
     x -= 1.
     return x`
'''

# Packages
###############################################################################

import os

from keras.applications.inception_v3 import preprocess_input
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

# Parameters and settings
###############################################################################


# Training data
###############################################################################


def idg_train():
    """Initialize an augmentation generator for training.

    Augmentation options:
        rescale: Rescaling factor; normalizing the data to [0:1]
        rotation_range: degree range for random rotations (integer)
        width_shift_range: range for random horizontal shifts (float)
        height_shift_range: range for random vertical shifts (float)
        shear_range: shear intensity (float)
        zoom_range: range for random zoom (float)
        horizontal_flip: randomly flip inputs horizontally (boolean)

    Returns:
        generator: A Keras image data generator object.

    """
    idg = ImageDataGenerator(preprocessing_function=preprocess_input,
                             rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True)

    return idg


def train_data_generator(X_train,
                         Y_train,
                         config):
    """Configueres the training generator for taking image and label data.

    Args:
        X_train (array): Image data as 4D numpy array.
        Y_train (array): Label data as 2D numpy array.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        generator: A image data generator with its `.flow` method applied.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_train = idg_train()

    # .flow() takes npdata en label arrays, and generates batches for
    # augmented/normalized data. Yields batches indefinitely, in an infinite
    # loop.
    idgen_train = idgen_train.flow(X_train,
                                   Y_train,
                                   batch_size=batch_size,
                                   seed=seed)
    return idgen_train


# Validation data
###############################################################################


def idg_val():
    """Initialize an augmentation generator for validation. Validation data
    should not be augmentatd, only correctly preprocessed for the model.

    Returns:
        generator: A Keras image data generator object.

    """
    idg = ImageDataGenerator(preprocessing_function=preprocess_input)

    return idg


def val_data_generator(X_val,
                       Y_val,
                       config):
    """Configueres the validation generator for taking image and label data.

    Args:
        X_val (array): Image data as 4D numpy array.
        Y_val (array): Label data as 2D numpy array.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        generator: A image data generator with its `.flow` method applied.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_val = idg_val()

    idgen_val = idgen_val.flow(X_val,
                               Y_val,
                               batch_size=batch_size,
                               seed=config.seed)

    return idgen_val

# Trainer
###############################################################################


def trainer(model,
            X_train,
            Y_train,
            X_val,
            Y_val,
            config,
            callbacks=None):
    """Initializes training on a model with training and validation image +
    label data as input.

    Args:
        model (Keras model instance): A Keras model instance.
        X_train (array): 4D numpy array training data for images.
        Y_train (array): 2D numpy array training data for labels.
        X_val (array): 4D numpy array validation data for images.
        Y_val (array): 2D numpy array validation data for labels.
        config (Bunch object): The JSON configuration Bunch object.
        callbacks (Callback object): One or a list of Keras Callback Objects.
            Defaults to `None`.

    Returns:
        training instance: Applies the `.fit_generator` method to a Keras
            model instance.

    """
    epochs = config.num_epochs
    batch_size = config.batch_size
    nb_X_train = len(X_train)

    train_data_gen = train_data_generator(X_train=X_train,
                                          Y_train=Y_train,
                                          config=config)

    val_data_gen = val_data_generator(X_val=X_val,
                                      Y_val=Y_val,
                                      config=config)

    model.fit_generator(train_data_gen,
                        validation_data=val_data_gen,
                        steps_per_epoch=(nb_X_train // batch_size),
                        epochs=epochs,
                        callbacks=callbacks)


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################


def train_data_generator_dir(data_dir, shottype, config):

    batch_size = config.batch_size
    seed = config.seed
    idgen_train = idg_train()

    idgen_train = idgen_train.flow_from_directory(
        directory=os.path.join('data', data_dir, 'images', shottype, '1-training'),
        target_size=(299, 299),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=batch_size,
        seed=1
    )

    return idgen_train

def val_data_generator_dir(data_dir, shottype, config):

    batch_size = config.batch_size
    seed = config.seed
    idgen_val = idg_val()

    idgen_val = idgen_val.flow_from_directory(
        directory=os.path.join('data', data_dir, 'images', shottype, '2-validation'),
        target_size=(299, 299),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=batch_size,
        seed=1
    )

    return idgen_val

def trainer_dir(model, data_dir, shottype, config, callbacks=None):
    epochs = config.num_epochs
    batch_size = config.batch_size
    train_data_gen_dir = train_data_generator_dir(data_dir, shottype, config)
    val_data_gen_dir = val_data_generator_dir(data_dir, shottype, config)

    model.fit_generator(generator=train_data_gen_dir,
                        steps_per_epoch=32,
                        epochs=epochs,
                        validation_data=val_data_gen_dir,
                        validation_steps=32,
                        callbacks=callbacks)

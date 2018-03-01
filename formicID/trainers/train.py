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
pixels between -1 and 1, samplewise and performs the following calculation:
`x /= 127.5
 x -= 1.
 return x`
'''

# Packages
###############################################################################

from keras.applications.inception_v3 import preprocess_input
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

# Parameters and settings
###############################################################################


# Training data
###############################################################################


def idg_train():
    """Short summary.

    Augmentation arguments:
        rescale: Rescaling factor; normalizing the data to [0:1]
        rotation_range: degree range for random rotations (integer)
        width_shift_range: range for random horizontal shifts (float)
        height_shift_range: range for random vertical shifts (float)
        shear_range: shear intensity (float)
        zoom_range: range for random zoom (float)
        horizontal_flip: randomly flip inputs horizontally (boolean)

    Returns:
        type: Description of returned object.

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
    """Short summary.

    Args:
        X_train (type): Description of parameter `X_train`.
        Y_train (type): Description of parameter `Y_train`.
        batch_size (type): Description of parameter `batch_size`.
        epochs (type): Description of parameter `epochs`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

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
    """Short summary.

    Returns:
        type: Description of returned object.

    """
    idg = ImageDataGenerator(preprocessing_function=preprocess_input)

    return idg


def val_data_generator(X_val,
                       Y_val,
                       config):
    """Short summary.

    Args:
        X_val (type): Description of parameter `X_val`.
        Y_val (type): Description of parameter `Y_val`.
        batch_size (type): Description of parameter `batch_size`.
        epochs (type): Description of parameter `epochs`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

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
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        X_train (type): Description of parameter `X_train`.
        Y_train (type): Description of parameter `Y_train`.
        X_val (type): Description of parameter `X_val`.
        Y_val (type): Description of parameter `Y_val`.
        callbacks (type): Description of parameter `callbacks`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

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

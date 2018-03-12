###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                             Build a neural network                          #
#                                                                             #
###############################################################################
'''Description:
This script contains code for building a neural network using Keras' Sequential
model. The class has a `.build` and `.compile` attribute which needs to be
called when instantiaitng the model.
'''
# Packages
###############################################################################
from keras.layers import (Activation, Conv2D, Dense, Dropout, Flatten,
                          MaxPooling2D)
from keras.models import Sequential

# Parameters and settings
###############################################################################


# Build the network
###############################################################################
def build_model(config, num_species, input_shape=(None, None, 3)):
    """Create a model with the architecture below. Afterwards the model needs
    to be compiled.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        num_species (int): The number of species, needed for the last layer.
        input_shape (int): list of image height and width, with channels=last.

    Returns:
        Keras model instance: Returns an uncompiled Keras model instance.

    """
    learning_rate = config.learning_rate
    dropout = config.dropout
    optimizer = config.optimizer

    model = Sequential()

    model.add(Conv2D(32, (3, 3),
                     padding='same',
                     input_shape=input_shape))
    model.add(Activation('relu'))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))

    model.add(Dense(num_species))
    model.add(Activation('softmax'))

    logging.info('The model has been build succesfully.')

    return model

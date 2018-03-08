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
def build_model(config, input_shape, num_species):
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
    model.add(Dropout(dropout))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))

    model.add(Dense(num_species))
    model.add(Activation('softmax'))

    return model

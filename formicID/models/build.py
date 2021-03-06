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
"""Description:
This script contains code for building a neural network using Keras' Sequential
model. The build could be loaded in the `models/models.py` file.
"""

# Packages
###############################################################################

# Deeplearning tools imports
from keras.layers import Activation
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import MaxPooling2D
from keras.models import Sequential

# Build the network
###############################################################################


def build_model(config, num_species, input_shape=(None, None, 3)):
    """Create a model with the architecture below. Afterwards the model needs
    to be compiled.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        num_species (int): The number of species, needed for the last layer.
        input_shape (int): list of image height and width, with channels=last.
            Defaults to (None, None, 3).

    Returns:
        Keras model instance: Returns an uncompiled Keras model instance.

    """
    dropout = config.dropout
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
    model.add(Activation("relu"))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(Activation("relu"))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation("relu"))
    model.add(Dropout(dropout))

    model.add(Dense(num_species))
    model.add(Activation("softmax"))

    logging.info("The model has been build succesfully.")

    return model

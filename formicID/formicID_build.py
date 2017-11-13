################################################################################
#                                                                              #
#                        FormicID Build and Compile                            #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from keras.models import Sequential  # for creating the model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, Adam, Nadam
from keras import backend as K


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
NUM_SPECIES = 3  # Todo: implement NUM_SPECIES from _train.py file

IMG_HEIGHT, IMG_WIDTH = 120, 148  # input for height and width

if K.image_data_format() == 'channels_first':
    input_shape = (3, IMG_HEIGHT, IMG_WIDTH)
else:
    input_shape = (IMG_HEIGHT, IMG_WIDTH, 3)

DROPOUT = 0.5


# Build the network
# //////////////////////////////////////////////////////////////////////////////
class neuralNetwork(object):
    """
    A neural netowrk model

    Attributes:
        input_shape: a tuple of IMG_HEIGHT, IMG_WIDTH and 3 channels
    """
    def __init__(self, NUM_SPECIES, input_shape, optimizer):
        """
        returns a neural network model. The input_shape needs to be specified
        """
        self.NUM_SPECIES = NUM_SPECIES
        self.input_shape = input_shape
        self.optimizer = optimizers

    def build_neural_network():
        """

        """
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(DROPOUT))
        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(DROPOUT))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(DROPOUT))
        model.add(Dense(NUM_SPECIES))
        model.add(Activation('softmax'))  # or use svm?

        print("Model was build succesfully.")
        return model

    def compile_neural_network(model, optimizer):
        """

        """
        if optimizer == "SGD":
            opt = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        if optimizer == "RMSprop":
            opt = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
        if optimizer == "Nadam":
            opt = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08,
            schedule_decay=0.004)

        model.compile(loss='categorical_crossentropy',
                      optimizer=opt,
                      metrics=['accuracy', 'top_k_categorical_accuracy'])
        print("Model was compiled succesfully.")
        return model

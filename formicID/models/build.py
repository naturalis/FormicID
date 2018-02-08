################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                             Build a neural network                           #
#                                                                              #
################################################################################
'''
Description:
<placeholder txt>
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////
from keras.models import Sequential  # for creating the model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, Adam, Nadam



# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////


# Build the network
# //////////////////////////////////////////////////////////////////////////////
class neuralNetwork(object):
    """
    A neural netowrk model

    Attributes:
        input_shape: a tuple of img_height, img_width and 3 channels
        dropout: a percentage of dropout
        num_species: a integer of the number of species
        optimizer: either 'SGD', 'RMSprop' or 'Nadam'.

    """
    def __init__(self, dropout, input_shape, num_species, optimizer):
        """
        # Returns
            A neural network model. The input_shape needs to be specified
        """
        self.dropout = dropout
        self.input_shape = input_shape
        self.num_species = num_species
        self.optimizer = optimizer

    def build_neural_network(self):
        """
        # Returns
            A keras model.
        """
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(self.dropout))
        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(self.dropout))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(self.dropout))
        model.add(Dense(self.num_species))
        model.add(Activation('softmax'))  # or use svm?

        if self.optimizer == "SGD":
            opt = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        if self.optimizer == "RMSprop":
            opt = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
        if self.optimizer == "Nadam":
            opt = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08,
            schedule_decay=0.004)

        model.compile(loss='categorical_crossentropy',
                      optimizer=opt,
                      metrics=['accuracy', 'top_k_categorical_accuracy'])
        print("Model was build and compiled succesfully.")
        return model

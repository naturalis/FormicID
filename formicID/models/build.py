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
from keras.models import Sequential  # for creating the model
from keras.optimizers import SGD, Adam, Nadam, RMSprop

# Parameters and settings
###############################################################################


# Build the network
###############################################################################
class neuralNetwork(object):
    def __init__(self, config, input_shape, num_species):
        """A neural network model. The input_shape needs to be specified.

        Args:
            dropout (type): a percentage of dropout.
            input_shape (type): image height, width and depth.
            num_species (type): an integer of the number of species.
            optimizer (type): either 'SGD', 'RMSprop' or 'Nadam'.

        Returns:
            type: Description of returned object.

        """
        # super(neuralNetwork, self).__init__(config)
        self.config
        self.input_shape = input_shape
        self.num_species = num_species
        self.optimizer = optimizer
        self.build()
        self.compile()

    def build(self):
        """Short summary.

        Returns:
            type: Description of returned object.

        """
        model = Sequential()
        model.add(Conv2D(32, (3, 3),
                        padding='same',
                        input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(self.configdropout))
        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(self.config.dropout))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(self.config.dropout))
        model.add(Dense(self.num_species))
        model.add(Activation('softmax'))
        print("Model is build succesfully.")
        return model


    def compile(self):
        if self.config.optimizer == "SGD":
            opt = SGD(lr=1e-2,
                      decay=1e-6,
                      momentum=0.9,
                      nesterov=True)
        if self.config.optimizer == "RMSprop":
            opt = RMSprop(lr=0.001,
                          rho=0.9,
                          epsilon=1e-08,
                          decay=0.0)
        if self.config.optimizer == "Nadam":
            opt = Nadam(lr=0.002,
                        beta_1=0.9,
                        beta_2=0.999,
                        epsilon=1e-08,
                        schedule_decay=0.004)

        model.compile(loss='categorical_crossentropy',
                      optimizer=opt)
                      # metrics=['accuracy', ',ae']

        print("Model is compiled succesfully.")

        return self

    # def train(self):
    #     self.fit_generator(train_data_gen,
    #                        validation_data=val_data_gen,
    #                        steps_per_epoch=5,
    #                        epochs=self.config.num_epochs, callbacks=build_tensorboard(model_formicID))

################################################################################
#                                                                              #
#                              FormicID input                                  #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from keras.models import Sequential  # for creating the model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////

"""
Define model architecture
Forward pass and backward pass (backpropagation)
    1.	Sequential model()
        a.	Convolutional--> Dropout--> Convolutional and Max Pooling-->
        Convolutional--> Dropout--> Convolutional and Max Pooling-->
        Convolutional--> Dropout--> Convolutional and Max Pooling--> flatten-->
        dropout--> fully connected--> dropout--> fully connected--> dropout-->
        fully connected

        also need batch normalization, usually after FC and before
        nonlinearity, you want to have this a lot, IMPORTANT!
    2.	Convolution (Convolution2D)
        a.	Filter size
        b.	Stride
        c.	Padding
        d.	Bias
        e.	What is the input and output dimension?
    3.	Maxpooling2D
        a.	Pool size
        b.	Stride
        c.	Padding
        d.	What is the input and output dimension?
    4.	Dense layers (fully connected)
    5.	Kernel initializer (weights)
    6.	Bias initializer (weights)
    7.	Dropout
        a.	Rate
        b.	Noise_shape()
            i.	batch_size, 1, features
        c.	Seed
    8.	Which activations?
        a.	First try ReLU
    9.	Flatten() layer
        a.	Flattens the input
        b.	Why?
    10.	Reshape() layer
        a.	Reshapes the input
        b.	Why?
    11.	Batch_size and batch_shape?
"""

model = Sequential()

# first layers needs to specify the input_shape. Following layers will reshape
model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(DROPOUT_P))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(DROPOUT_P))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(DROPOUT_P))
model.add(Dense(num_species))
model.add(Activation('softmax')) # or use svm?

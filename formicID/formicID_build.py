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
num_species = 3  # species

img_height, img_width = 120, 148  # input for width and height

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# Build the network
# //////////////////////////////////////////////////////////////////////////////

def build_neural_network():
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

    # First layers needs to specify the input_shape
    # Following layers will reshape
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Dropout(0.5))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))

    model.add(Dropout(0.5))

    model.add(Dense(num_species))
    model.add(Activation('softmax'))  # or use svm?

    print("Model was created succesfully")
    return model


# Compile the network
# //////////////////////////////////////////////////////////////////////////


# SGD can also be an optimzer
optimzer_sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)

optimizer_rmsprpop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08,
                                              decay=0.0)
# It is recommended to leave the parameters of this optimizer at their default
# values (except the learning rate, which can be freely tuned).
# This optimizer is usually a good choice for recurrent neural networks.
# very effective
# cite slide 29 of Lecture 6 of Geoff Hinton’s Coursera class.

optimzer_nadam = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999,
                                        epsilon=1e-08, schedule_decay=0.004)
# Default parameters follow those provided in the paper. It is recommended to
# leave the parameters of this optimizer at their default values.


def compile_neural_network(model):
    """
    Compiling of the model = configuring the learning process
        Before training a model, you need to configure the learning process, which
        is done via the compile method.
        1.	Model.compile()
            a.	Learning rate?
                i. In training deep networks, it is usually helpful to anneal the
                learning rate over time. Use step decay
            b.	Decay = learning rate / epoch
            c.	Loss function (e.g. softmax)
            d.	Metric function
                i. For any classification problem you will want to set this to
                metrics=['accuracy']
            e.	Optimizer function
                i. sgd = Stochastic gradient descent optimizer
                ii. In practice Adam is currently recommended as the default
                algorithm to use, and often works slightly better than RMSProp.
                However, it is often also worth trying SGD+Nesterov Momentum as an
                alternative.]
        2. Visualizing the model optimization using TensorBoard
    """
    #   when using the categorical_crossentropy loss, your targets should be in
    #   categorical format (e.g. if you have 10 classes, the target for each
    #   sample should be a 10-dimensional vector that is all-zeros expect for a
    #   1 at the index corresponding to the class of the sample). In order to
    #   convert integer targets into categorical targets, you can use the Keras
    #   utility to_categorical

    # top_k_categorical_accuracy --> default value = 5
    # code to change to top 3
    # top3_acc = functools.partial(keras.metrics.top_k_categorical_accuracy,k=3)
    # top3_acc.__name__ = 'top3_acc'

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimzer_nadam,
                  metrics=['accuracy', 'top_k_categorical_accuracy'])
    print("Model was compiled Succesfully")
    return model

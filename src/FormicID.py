#!/usr/bin/env python

__author__ = "Marijn Boer"
#__copyright__ = ""
__credits__ = ["Marijn Boer"]
#__license__ = ""
__version__ = "0.1"
__maintainer__ = "Marijn Boer"
__email__ = "marijn.j.a.boer@gmail.com"
__status__ = "Production"

################################################################################
# FormicID                                                                     #
# Species identification from AntWeb images using a convolutional neural       #
# network.                                                                     #
# Version: 0.1b                                                                #
################################################################################

"""
Link to the cloud?
Openstack from naturalis!
"""

from __future__ import print_function
# allow use of print as a function. Needed when loading in Python 2.x

"""
Import libraries and modules·
    1.	Keras
        a.	from keras.models import Sequential
        b.	Core layers: from keras.layers import Dense, Dropout, Activation,
        Flatten
        c.	CNN layers: from keras.layers import Convolution2D, MaxPooling2D
    2.	Numpy
        a.	e.g. np.random.seed
"""
import keras
from keras.models import Sequential  # for creating the model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator #for image augmentation
from keras import backend as K

import numpy
import os  # provides a way of using operating system dependent functionality.
import time
import matplotlib.pyplot as plt #for plotting images°
import cv2 # for importing and converting imagees



"""
Some settings and hyperparameters
Verbose:
    0 for no logging to stdout,
    1 for progress bar logging,
    2 for one log line per epoch.
"""
SEED = 63
np.random.seed(SEED)

img_width, img_height = 150, 150 #input for width and height

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# batch size = the number of training examples in one forward/backward pass.
# The higher the batch size, the more memory space you'll need.
BATCH_SIZE = 16

num_species =  2 # species

# one epoch = one forward pass and one backward pass of all the training
# examples
EPOCHS = 100

DATA_AGUMENTATION =  # True/False

NUM_PREDICTIONS =
#save_dir = os.path.join(os.getcwd(), 'saved_models')
#model_name = 'keras_formicidae_trained_model.h5'

DROPOUT_P = 0.25  # probability of keeping a unit active. higher = less dropout
# 0.5 is a reasonable default

# number of iterations = number of passes, each pass using [batch size] number
# of examples. To be clear, one pass = one forward pass + one backward pass (we # do not count the forward pass and backward pass as two different passes).


save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_FormicID_trained_model.h5'

"""
Importing images - Acquiring data and put them in variables
    1.	Download images with labels from AntWeb API
        a.	Json format
    2.	Pickle images to pickle objects?

Load ready-made data
    1.	directory
    2.	dimensions of the images?
        a.	It has 3 depth for sure
        b.	Create image_bytes = result.height * result.width * result.depth ?
        c.	record_bytes = label_bytes + image_bytes ?
    3.	(X_training, Y_traning), (X_test, Y_test)
"""

keras.utils.get_file() # can use url?

train_data_dir = '/Users/nijram13/Google Drive/4. Biologie/Studie   Biologie/Master Year 2/Internship CNN/probeersel/data/train'
validation_data_dir = '/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/probeersel/data/validation'

X_train = []
Y_train = []

X_test = []
Y_test = []

number_train_samples = 6  # number of training samples
number_validation_samples = 4  # number of validation/test samples


"""
hyperparameters optimization
    Use Bayesian Hyperparameter Optimization for hyperparameters:
        the initial learning rate
        learning rate decay schedule (such as the decay constant)
        regularization strength (L2 penalty, dropout strength)
"""
# Code

"""
pre-process input data
The recommended preprocessing is to center the data to have mean of zero,
and normalize its scale to [-1, 1] along each feature
    1.	subsample data
    2.	normalize data
        a. divide by 255.0?
    3.	transpose data, so that the channels come first # see lines above
    4.	package data into a dictionary
"""
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

"""
Data augumentation
with keras modules
"""
ImageDataGenerator()
# https://keras.io/preprocessing/image/
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

"""
pre-process class labels
    1.	How many class labels?
    2.	For test and training sets
"""
# code
num_species = Y_test.shape[1]

"""
Visualize 10 random labels with 10 images
"""
# code

"""
Weight and batch initialization and regularization --> to get loss as low
as possible
    In practice, the current recommendation is to use ReLU units and use
    the w = np.random.randn(n) * sqrt(2.0/n), as discussed in He et al..

    Regularization
        Use L2 regularization and dropout (the inverted version)!

    Batch normalization
        Normalize the activations of the previous layer at each batch, i.e.
        applies a transformation that maintains the mean activation close
        to 0 and the activation standard deviation close to 1.
"""
n =  # number of inputs
w = np.random.randn(n) * sqrt(2.0 / n)  # where n is the number of its inputs

keras.layers.BatchNormalization()

#from keras.regularizers import l2
#model.add(Dense(64, 64, W_regularizer = l2(.01)))

#noise layer?
keras.layers.GaussianNoise(stddev)

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
# example of a simple deep CNN as a function

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
model.add(Activation('softmax'))

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
            alternative.
"""
# SGD can also be an optimzer
optimzer_sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)

optimizer_rmsprpop = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08,
                                              decay=0.0)
# It is recommended to leave the parameters of this optimizer at their default
# values (except the learning rate, which can be freely tuned).
# This optimizer is usually a good choice for recurrent neural networks.
# very effective
# cite slide 29 of Lecture 6 of Geoff Hinton’s Coursera class.

optimzer_nadam = keras.optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999,
                                        epsilon=1e-08, schedule_decay=0.004)
# Default parameters follow those provided in the paper. It is recommended to
# leave the parameters of this optimizer at their default values.


# top_k_categorical_accuracy --> default value = 5
# code to change to top 3
# top3_acc = functools.partial(keras.metrics.top_k_categorical_accuracy, k=3)
# top3_acc.__name__ = 'top3_acc'

model.compile(loss='categorical_crossentropy',
              optimizer=optimzer_nadam ,
              metrics=['accuracy','top_k_categorical_accuracy']) #

#   when using the categorical_crossentropy loss, your targets should be in
#   categorical format (e.g. if you have 10 classes, the target for each
#   sample should be a 10-dimensional vector that is all-zeros expect for a
#   1 at the index corresponding to the class of the sample). In order to
#   convert integer targets into categorical targets, you can use the Keras
#   utility to_categorical


"""
Training the model (by using the fit function)
    1.	Connect to cloud
    2.	Fit() function
    3.	How many epoch?
        a.	Think about hundreds of thousands
        b.	Every epoch, check training and validation accuracy and decay learning rate
"""
model.fit()

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=BATCH_SIZE,
    class_mode='binary')




"""
Evaluate model on test data
    1.	Evaluate()
        a.	Computes the loss on some input data, batch by batch.
    2.	Score of the model
    3.	Accuracy of the training model
    4.	Speed of the model
    5.	How long is training time?
    6.	How many steps and epochs?
    7.	Iterations?
    8.	Top 5 or top 1 accuracy?
"""
model.evaluate()

model.predict()

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(150, 150),
    batch_size=BATCH_SIZE,
    class_mode='binary')

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])

"""
Predict
"""
model.fit_generator(
    train_generator,
    steps_per_epoch=2000,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=800)


"""
Model visualization?
"""
# Save model and weights
if not os.path.isdir(save_dir):
    os.makedirs(save_dir) #if "saved models" folder is not present, make one
model_path = os.path.join(save_dir, model_name) #path to the model
model.save(model_path) #save the model to the model path
print('Saved trained model at %s ' % model_path) #print if it worked

keras.utils.plot_model() #needs graphvidz and pydot package


################################################################################
# if this code is seen as the 'main page' then print the version of Keras
if __name__ == '__main__':
    print('Keras version: {}'.format(keras.__version__))

#!/usr/bin/env python

################################################################################
# FormicID                                                                     #
# Species identification from AntWeb images using a convolutional neural       #
# network.                                                                     #
# Version: 0.1b                                                                #
################################################################################

from __future__ import print_function
# allow use of print as a function. Needed when loading in Python 2.x

"""
Importing libraries and modules
"""
import keras
from keras.layers import BatchNormalization
from keras import backend as K
from keras.callbacks import TensorBoard

from src.FormicID_build import build_neural_network

import numpy
import os  # provides a way of using operating system dependent functionality.
import time # to keep track of time and create time based log folders
import matplotlib.pyplot as plt  # for plotting images°
import cv2  # for importing and converting imagees

"""
Link to the cloud?
Openstack from Naturalis!
"""

"""
Some settings and hyperparameters
Verbose:
    0 for no logging to stdout,
    1 for progress bar logging,
    2 for one log line per epoch.
"""
SEED = 63
np.random.seed(SEED)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# batch size = the number of training examples in one forward/backward pass.
# The higher the batch size, the more memory space you'll need.
BATCH_SIZE = 16



# one epoch = one forward pass and one backward pass of all the training
# examples
EPOCHS = 100

DATA_AGUMENTATION =  # True/False

NUM_PREDICTIONS =
#save_dir = os.path.join(os.getcwd(), 'saved_models')
#model_name = 'keras_formicidae_trained_model.h5'

DROPOUT_P = 0.50  # probability of keeping a unit active. higher = less dropout
# 0.5 is a reasonable default

# number of iterations = number of passes, each pass using [batch size] number
# of examples. To be clear, one pass = one forward pass + one backward pass (we # do not count the forward pass and backward pass as two different passes).


save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'FormicID_keras_trained_model.h5'

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

Use FormicidID_input
train_generator

keras.utils.get_file()  # can use url?

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
#X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
#X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)
#X_train = X_train.astype('float32')
#X_test = X_test.astype('float32')
#X_train /= 255
#X_test /= 255


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
as possible  and Data augumentation
    In practice, the current recommendation is to use ReLU units and use
    the w = np.random.randn(n) * sqrt(2.0/n), as discussed in He et al..

    Regularization
        Use L2 regularization and dropout (the inverted version)!

    Batch normalization
        Normalize the activations of the previous layer at each batch, i.e.
        applies a transformation that maintains the mean activation close
        to 0 and the activation standard deviation close to 1.

    Common pattern for regularization:
        Dropout > Batch normalization > Data Augmentation > Dropconnect

"""
n =  # number of inputs
w = np.random.randn(n) * sqrt(2.0 / n)  # where n is the number of its inputs

keras.layers.BatchNormalization()

#from keras.regularizers import l2
#model.add(Dense(64, 64, W_regularizer = l2(.01)))

# Noise layer?
# keras.layers.GaussianNoise(stddev)

# Data augmentation
"""
Is already in 'FormicID_input' file
ImageDataGenerator()
# https://keras.io/preprocessing/image/
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

"""

# Dropconnect?




"""
Training Set:
    this data set is used to adjust the weights on the neural network.

Validation Set:
    this data set is used to minimize overfitting. You're not
    adjusting the weights of the network with this data set, you're just
    verifying that any increase in accuracy over the training data set actually
    yields an increase in accuracy over a data set that has not been shown to
    the network before, or at least the network hasn't trained on it (i.e.
    validation data set). If the accuracy over the training data set increases,
    but the accuracy over then validation data set stays the same or decreases,
    then you're overfitting your neural network and you should stop training.

    you tune parameters according to these results.?

Testing Set:
    this data set is used only for testing the final solution in order
    to confirm the actual predictive power of the network.

            for each epoch
                for each training data instance
                    propagate error through the network
                    adjust the weights
                    calculate the accuracy over training data
                for each validation data instance
                    calculate the accuracy over the validation data
                if the threshold validation accuracy is met
                    exit training
                else
                    continue training

"""

"""
Training the model (by using the fit function)
    1.	Connect to cloud
    2.	Fit() function
        a. fit_generator: Fits the model on data generated batch-by-batch by a
        Python generator.
    3.	How many epoch?
        a.	Think about hundreds of thousands
        b.	Every epoch, check training and validation accuracy and decay
        learning rate
"""
model.fit() #training

model.fit_generator(
    train_generator,
    steps_per_epoch=2000,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=800,
    callbacks = Callbacks_Tensorboard)


# train_generator = train_datagen.flow_from_directory(
#    train_data_dir,
#    target_size=(img_width, img_height),
#    batch_size=BATCH_SIZE,
#    class_mode='binary',
#    callbacks = Callbacks_Tensorboard)

# validation
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(150, 150),
    batch_size=BATCH_SIZE,
    class_mode='binary')

"""
Evaluate model on test data
    1.	Evaluate()
        a.	.evaluate() computes the loss based on the input you pass it, along
        with any other metrics that you requested in the metrics param when you
        compiled your model
    2.	Score of the model
    3.	Accuracy of the training model
    4.	Speed of the model
    5.	How long is training time?
    6.	How many steps and epochs?
    7.	Iterations?
    8.	Top 5 or top 1 accuracy?
    9   Visualize how the model performs with tensorboard
"""

# evaluates the loss based on the input
model.evaluate()

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])

# graphs:
# loss curve (y:loss, x: epochs),
# train and val accuracy vs epoch


"""
Predict:
    Generates output predictions for the input samples (the labels)
"""
predictions = model.predict(x_test)
print('First prediction:', predictions[0]
print('Second prediction:', predictions[1]
print('Third prediction:', predictions[2]
print('Fourth prediction:', predictions[3]
print('Fifth prediction:', predictions[4]


"""
Model visualization?
"""
# Save model and weights
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)  # if "saved models" folder is not present, make one
model_path = os.path.join(save_dir, model_name)  # path to the model
model.save(model_path)  # save the model to the model path
print('Saved trained model at %s ' % model_path)  # print if it worked

# plot the model
keras.utils.plot_model()  # needs graphvidz and pydot package


################################################################################
# if this code is seen as the 'main page' then print the version of Keras
if __name__ == '__main__':
    print('Keras version: {}'.format(keras.__version__))

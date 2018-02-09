################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                             Load existing models                             #
#                                                                              #
################################################################################
'''
Description:
Import 4 existing neural netwerks from the Keras library
(https://keras.io/applications/), all in their own function. These could be
loaded in other scripts.

From the Keras documentation:
All of these architectures (except Xception) are compatible with both
TensorFlow and Theano, and upon instantiation the models will be built
according to the image data format set in your Keras configuration file at
~/.keras/keras.json. For instance, if you have set
image_data_format=channels_last, then any model loaded from this repository
will get built according to the TensorFlow data format convention,
"Height-Width-Depth". The Xception model is only available for TensorFlow, due
to its reliance on SeparableConvolution layers.
'''

# Packages
# //////////////////////////////////////////////////////////////////////////////
from keras.applications.resnet50 import ResNet50  # ResNet based
from keras.applications.densenet import DenseNet169  # ResNet based
from keras.applications.inception_v3 import InceptionV3  # Inception based
from keras.applications.xception import Xception  # Inception based

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////


# Model Settings
# //////////////////////////////////////////////////////////////////////////////


# ResNet50
# //////////////////////////////////////////////////////////////////////////////


def model_resnet50(include_top, weights, input_tensor, input_shape, pooling, classes):
    '''
    ResNet50 model, with weights pre-trained on ImageNet.

    This model is available for both the Theano and TensorFlow backend, and can be built both with 'channels_first' data format (channels, height, width) or 'channels_last' data format (height, width, channels).

    The default input size for this model is 224x224.
    '''
    model = ResNet50(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes)
    return model


# DenseNet169
# //////////////////////////////////////////////////////////////////////////////


def model_densenet169(include_top, weights, input_tensor, input_shape, pooling, classes):
    '''
    Optionally loads weights pre-trained on ImageNet. Note that when using TensorFlow, for best performance you should set image_data_format='channels_last' in your Keras config at ~/.keras/keras.json.

    The model and the weights are compatible with TensorFlow, Theano, and CNTK. The data format convention used by the model is the one specified in your Keras config file.
    '''
    model = DenseNet169(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes)
    return model


# InceptionV3
# //////////////////////////////////////////////////////////////////////////////


def model_inceptionv3(include_top, weights, input_tensor, input_shape, pooling, classes):
    '''
    Inception V3 model, with weights pre-trained on ImageNet.

    This model is available for both the Theano and TensorFlow backend, and can be built both with 'channels_first' data format (channels, height, width) or 'channels_last' data format (height, width, channels).

    The default input size for this model is 299x299.
    '''
    model = InceptionV3(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes)
    return model


# Xception
# //////////////////////////////////////////////////////////////////////////////


def model_xception(include_top, weights, input_tensor, input_shape, pooling, classes):
    '''
    Xception V1 model, with weights pre-trained on ImageNet.

    On ImageNet, this model gets to a top-1 validation accuracy of 0.790 and a top-5 validation accuracy of 0.945.

    Note that this model is only available for the TensorFlow backend, due to its reliance on SeparableConvolution layers. Additionally it only supports the data format 'channels_last' (height, width, channels).

    The default input size for this model is 299x299.
    '''
    model = Xception(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling=pooling,
        classes=classes)
    return model

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
'''Description:
Using this script 4 existing neural netwerks from the Keras library
(https://keras.io/applications/) can be imported in a class object. This class has four methods to call in order to load the 4 models.

The models are:
    - ResNet50
    - DenseNet169
    - InceptionV3
    - Xception

```From the Keras documentation:
All of these architectures (except Xception) are compatible with both
TensorFlow and Theano, and upon instantiation the models will be built
according to the image data format set in your Keras configuration file at
~/.keras/keras.json. For instance, if you have set
image_data_format=channels_last, then any model loaded from this repository
will get built according to the TensorFlow data format convention,
"Height-Width-Depth". The Xception model is only available for TensorFlow, due
to its reliance on SeparableConvolution layers.```
'''
# Packages
################################################################################

from keras.applications.densenet import DenseNet169
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.applications.xception import Xception
from keras.layers import Dense, GlobalAveragePooling2D, Input
from keras.models import Model
from keras.optimizers import SGD, Adam, Nadam, RMSprop

# Parameters and settings
################################################################################


# Models
################################################################################


class modelLoad():
    def __init__(self, config):
        self.config = config

    def model_compile(self, model):
        optimizer = self.config.optimizer
        learning_rate = self.config.learning_rate

        if optimizer == "Nadam":
            opt = Nadam(lr=learning_rate,
                        beta_1=0.9,
                        beta_2=0.999,
                        epsilon=1e-08,
                        schedule_decay=0.004)

        model_comp = model.compile(loss='sparse_categorical_crossentropy',
                                   optimizer=opt)
        return model_comp

    def model_inceptionv3(self, num_classes):
        '''Inception V3 model, with weights pre-trained on ImageNet.

        This model is available for both the Theano and TensorFlow backend, and
        can be built both with 'channels_first' data format (channels, height,
        width) or 'channels_last' data format (height, width, channels).

        The default input size for this model is 299x299.
        '''
        base_model = InceptionV3(include_top=False,
                                 weights=None,
                                 input_tensor=None,
                                 input_shape=None,
                                 pooling=None,
                                 classes=None)

        # add a global spatial average pooling layer
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        # let's add a fully-connected layer
        x = Dense(1024, activation='relu')(x)
        # and a logistic layer with num_species
        predictions = Dense(num_classes, activation='softmax')(x)

        # this is the model we will train
        end_model = Model(inputs=base_model.input, outputs=predictions)

        return end_model

    # TODO: Finetune the other models.
    # def model_resnet50():
    #     '''ResNet50 model, with weights pre-trained on ImageNet.
    #
    #     This model is available for both the Theano and TensorFlow backend, and
    #     can be built both with 'channels_first' data format (channels, height,
    #     width) or 'channels_last' data format (height, width, channels).
    #
    #     The default input size for this model is 224x224.
    #     '''
    #     base_model = ResNet50(include_top=False,
    #                           weights=None,
    #                           input_tensor=None,
    #                           input_shape=None,
    #                           pooling=None,
    #                           classes=None)
    #
    #     # this is the model we will train
    #     end_model = Model(inputs=base_model.input, outputs=predictions)
    #
    #     return end_model
    #
    # def model_densenet169():
    #     '''Optionally loads weights pre-trained on ImageNet. Note that when
    #     using TensorFlow, for best performance you should set
    #     image_data_format='channels_last' in your Keras config at
    #     ~/.keras/keras.json.
    #
    #     The model and the weights are compatible with TensorFlow, Theano, and
    #     CNTK. The data format convention used by the model is the one specified
    #     in your Keras config file.
    #     '''
    #     base_model = DenseNet169(include_top=False,
    #                              weights=None,
    #                              input_tensor=None,
    #                              input_shape=None,
    #                              pooling=None,
    #                              classes=None)
    #     end_model = Model(inputs=base_model.input, outputs=predictions)
    #
    #     return end_model
    #
    # def model_xception():
    #     '''Xception V1 model, with weights pre-trained on ImageNet.
    #
    #     On ImageNet, this model gets to a top-1 validation accuracy of 0.790
    #     and a top-5 validation accuracy of 0.945.
    #
    #     Note that this model is only available for the TensorFlow backend, due
    #     to its reliance on SeparableConvolution layers. Additionally it only
    #     supports the data format 'channels_last' (height, width, channels).
    #
    #     The default input size for this model is 299x299.
    #     '''
    #     base_model = Xception(include_top=False,
    #                           weights=None,
    #                           input_tensor=None,
    #                           input_shape=None,
    #                           pooling=None,
    #                           classes=None)
    #
    #     end_model = Model(inputs=base_model.input, outputs=predictions)
    #
    #     return end_model

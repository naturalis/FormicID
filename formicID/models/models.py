###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                         Load Keras models applications                      #
#                                                                             #
###############################################################################
"""Description:
Using this script 5 existing neural netwerks from the Keras library
(https://keras.io/applications/) or `models/build.py` could be imported and or
build. Afterwards the model needs to be compiled using the compile function.

The models are:
    - ResNet50
    - DenseNet169
    - InceptionResNetV2
    - InceptionV3
    - Xception
    - Build

From the Keras documentation:
    All of these architectures (except Xception) are compatible with both
    TensorFlow and Theano, and upon instantiation the models will be built
    according to the image data format set in your Keras configuration file at
    ~/.keras/keras.json. For instance, if you have set
    image_data_format=channels_last, then any model loaded from this repository
    will get built according to the TensorFlow data format convention,
    "Height-Width-Depth". The Xception model is only available for TensorFlow,
    due to its reliance on SeparableConvolution layers.
"""

# Packages
###############################################################################

# Standard library imports
import logging
import os

# Deeplearning tools imports
from keras.applications.densenet import DenseNet169
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.applications.xception import Xception
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import GlobalAveragePooling2D
from keras.models import Model
from keras.layers import PReLU
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.optimizers import Nadam
from keras.optimizers import RMSprop

# FormicID imports
from models.build import build_model
from utils.logger import top_k_cat_accuracy
from utils.logger import rmse
from models.optimizer import Eve


# Load models
###############################################################################


def load_model(config):
    """Load a predesigned neural network application from the Keras library or
    the self-designed neural network from `models/build.py`. See text below
    for more information on the different models that can be loaded.

    Args:
        config (Bunch object): The JSON configuration Bunch object, which
            states the model to load, dropout and the correct dataset for
            counting the number of species.

    Returns:
        A Keras model instance.

    Model information:
        Build:
            This is the self-designed model from this research. For more
            information see `models/build.py`.

        InceptionV3:
            The default input size for this model is 299x299.

        InceptionResNetV2:
            The default input size for this model is 299x299.

        ResNet50 model:
            The default input size for this model is 224x224.

        DenseNet169:
            The data format convention used by the model is the one specified
            in your Keras config file.

        Xception V1:
            Note that this model is only available for the TensorFlow backend,
            due to its reliance on SeparableConvolution layers. Additionally
            it only supports the data format 'channels_last' (height, width,
            channels). The default input size for this model is 299x299.

    """
    model = config.model
    dataset = config.data_set
    dropout = config.dropout
    shottype = config.shottype
    data_dir = os.path.join("data", dataset, "json_files")
    num_species = sum(
        os.path.isfile(os.path.join(data_dir, i)) for i in os.listdir(data_dir)
    )
    if model not in [
        "InceptionV3",
        "InceptionResNetV2",
        "Xception",
        "ResNet50",
        "DenseNet169",
        "Build",
    ]:
        raise ValueError(
            "Model should be one of `InceptionV3`, `InceptionResNetV2`, "
            "`Xception`, `ResNet50` or `DenseNet169` or `Build`. Please "
            "set a correct model instead of {}.".format(model)
        )

    if model == "Build":
        end_model = build_model(
            config=config, input_shape=(299, 299, 3), num_species=num_species
        )
    else:
        if model == "InceptionV3":
            base_model = InceptionV3(
                include_top=False, weights="imagenet", classes=None
            )
        if model == "InceptionResNetV2":
            base_model = InceptionResNetV2(
                include_top=False, weights="imagenet", classes=None
            )
        if model == "ResNet50":
            base_model = ResNet50(
                include_top=False, weights="imagenet", classes=None
            )
        if model == "DenseNet169":
            base_model = DenseNet169(
                include_top=False, weights="imagenet", classes=None
            )
        if model == "Xception":
            base_model = Xception(
                include_top=False, weights="imagenet", classes=None
            )
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(dropout)(x)
        x = Dense(1024, activation="relu")(x)
        predictions = Dense(num_species, activation="softmax")(x)
        end_model = Model(inputs=base_model.input, outputs=predictions)
    logging.info("The model is build with success.")
    return end_model


# Compile a model
###############################################################################


def compile_model(model, config):
    """After building a Keras model, the model needs to be compiled.

    Args:
        model (keras model instance): A uncompiled Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        Keras model instance: a compiled Keras model instance.

    """
    optimizer = config.optimizer
    learning_rate = config.learning_rate
    if optimizer not in ["Nadam", "Adam", "SGD", "RMSprop", "Eve"]:
        raise ValueError(
            "The optimizer should be one of: `Nadam`, `Adam`, "
            "`SGD` or `RMSprop`"
        )

    if optimizer == "Eve":
        opt = Eve(
            lr=learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            beta_3=0.999,
            small_k=0.1,
            big_K=10,
            epsilon=1e-8,
            decay=0.0001,
            # clipnorm=1.,
            # clipvalue=0.5,
        )
    if optimizer == "Nadam":
        opt = Nadam(
            lr=learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-08,
            schedule_decay=0.004,
        )
    if optimizer == "Adam":
        opt = Adam(
            lr=learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=None,
            decay=0.0,
            amsgrad=False,
        )
    if optimizer == "SGD":
        opt = SGD(lr=learning_rate, decay=1e-6, momentum=0.9, nesterov=True)
    if optimizer == "RMSprop":
        opt = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-08, decay=0.0)
    if opt:
        model.compile(
            loss="categorical_crossentropy",
            optimizer=opt,
            metrics=[
                "accuracy",
                top_k_cat_accuracy,
                # rmse,
            ],
        )
    else:
        raise ValueError("There is no optimizer.")

    logging.info("The model is compiled with success.")

    return model

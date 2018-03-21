###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Utilitiies                                 #
#                                    Models                                   #
###############################################################################
'''Description:
This file has code utilities for handeling models.
'''

# Packages
###############################################################################

# Standard library imports
import logging
import os

# Deeplearning tools imports
import tensorflow as tf
from keras.models import Model
from keras.models import load_model
from keras.models import model_from_json
from keras.utils import multi_gpu_model
from keras.utils.vis_utils import plot_model

# Data tools imports
import h5py  # Needed for model.save()

# Graphical tools imports
import graphviz  # Needed for keras.utils.vis_utils.plot_model()
import pydot_ng  # Needed for keras.utils.vis_utils.plot_model()

from .utils import wd

# Parameters and settings
###############################################################################


# Model utilities
###############################################################################


def save_model(model, filename, config):
    """Saving a Keras model instance.

    Args:
        model (Keras model instance): A Keras model instance.
        filename (str): Name of the output filename.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        file: A `.h5` file of the model.

    """
    out = os.path.join(config.checkpoint_dir, filename)
    model.save(filepath=out)
    logging.info('The model has been saved and deleted from use.')
    del model


def load_model(filename, input_dir):
    """Loads a Keras model instance from a `.h5` file.

    Args:
        filename (Keras model instance): A Keras model instance.
        input_dir (path): the directory that holds the model.

    Returns:
        Keras model instance: A Keras model instance.

    """
    input_model = os.path.join(wd, input_dir, filename)
    model = load_model(input_model)
    logging.info('The model has been loaded.')
    return model


def weights_save(model, filename, config):
    """Saving the weights of a Keras model instance.

    Args:
        model (Keras model instance): A Keras model instance.
        filename (str): Description of parameter `filename`.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        file: A `.h5` file.

    """
    out = os.path.join(config.checkpoint_dir, filename)
    weights_saved = model.save_weights(filepath=out)
    logging.info('The weights have been saved.')


def weights_load(model, filename, input_dir):
    """Short summary.

    Args:
        model (Keras model instance): A Keras model instance.
        filename (str): Name of the output filename.
        input_dir (str): the directory that holds the weights.

    Returns:
        Keras model instance: A model with its weights initialized.

    """
    input_weights_input = os.path.join(wd, input_dir, filename)
    model.load_weights = load_weights_input(input_model)
    logging.info('The weights have been loaded.')
    return model


def model_summary(model):
    """Return a summary of Keras model intance.

    Args:
        model (Keras model instance): A Keras model instance.

    Returns:
        str: A summary

    """
    summary = model.summary()
    return summary


def model_config(model):
    """Extract the configuration of a Keras model instance.

    Args:
        model (Keras model instance): A Keras model instance.

    Returns:
        dict: A dictionary containing the configuration of the model

    """
    config = model.config()
    # Returns a dictionary containing the configuration of the model.
    return config


def model_from_config(config):
    """Load a Keras model instance from a configuration file.

    Args:
        config (JSON object): The config file that holds a Keras model instance.

    Returns:
        Keras model instance: A Keras model instance.

    """
    config = model.get_config()
    model = Model.from_config(config)
    return model


def model_architecture(model):
    """Save a Keras model instance to a JSON object.

    Args:
        model (Keras model instance): A Keras model instance.

    Returns:
        JSON: A JSON object.

    """
    json_object = model.to_json()
    return json_object


def model_from_architecture(json_object):
    """Load a Keras model instance from a JSON object.

    Args:
        json_object (JSON): A JSON object that describes a Keras model
            instance.

    Returns:
        Keras model instance: A Keras model instance.

    """
    model = model_from_json(json_object)
    return model


def model_visualization(model, config):
    """Saves an visualization of a Keras model instance as an image.

    Args:
        model (Keras model instance): A Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        file: An image `png` file.

    """
    filename = str(config.exp_name)
    output_dir = os.path.join(config.summary_dir, filename + '_model.png')
    logging.info('The model is saved in: {}'.format(output_dir))
    return plot_model(model=model,
                      to_file=output_dir,
                      show_shapes=True,
                      show_layer_names=True)


def make_multi_gpu(model, gpus=2):
    """Returns a Keras model instance that will train on a set number of GPUs.
    This function requires an uncompiled version of the Keras model instance.
    After compiling the output of this model the trainer can be used. The new
    batch_size should be the `gpus` * original `batch_size`.

    Args:
        model (Keras model instance): A Keras model instance.
        gpus (int): Sets the number of gpus to train on. Defaults to 4.

    Returns:
        Keras model instance: A multi GPU Keras model instance, uncompiled.

    """
    with tf.device('/cpu:0'):
        model = model
    gpu_model = multi_gpu_model(model=model, gpus=gpus)
    return multi_gpu_formicID

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
import os

import graphviz  # Needed for keras.utils.vis_utils.plot_model()
import h5py  # Needed for model.save()
import pydot_ng  # Needed for keras.utils.vis_utils.plot_model()
from keras.models import Model, load_model, model_from_json
from keras.utils.vis_utils import plot_model

# Parameters and settings
###############################################################################
wd = os.getcwd()

# Model utilities
###############################################################################


def save_model(model, filename, config):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        filename (type): Description of parameter `filename`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    out = os.path.join(config.checkpoint_dir, filename)
    model.save(filepath=out)
    print('The model has been saved and deleted from use.')
    del model


def load_model(filename, input_dir):
    """Short summary.

    Args:
        filename (type): Description of parameter `filename`.
        input_dir (type): Description of parameter `input_dir`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    input_model = os.path.join(wd, input_dir, filename)
    model = load_model(input_model)
    print('The model has been loaded.')
    return model


def weights_save(model, filename, config):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        filename (type): Description of parameter `filename`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    out = os.path.join(config.checkpoint_dir, filename)
    weights_saved = model.save_weights(filepath=out)
    print('The weights have been saved.')


def weights_load(model, filename, input_dir):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        filename (type): Description of parameter `filename`.
        input_dir (type): Description of parameter `input_dir`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    input_weights_input = os.path.join(wd, input_dir, filename)
    model.load_weights = load_weights_input(input_model)
    print('The weights have been loaded.')
    return model


def model_summary(model):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    summary = model.summary()
    return summary


def model_config(model):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    config = model.config()
    # Returns a dictionary containing the configuration of the model.
    return config


def model_from_config(config):
    """Short summary.

    Args:
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    config = model.get_config()
    model = Model.from_config(config)
    return model


def model_architecture(model):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    json_string = model.to_json()
    return json_string


def model_from_architecture(json_string):
    """Short summary.

    Args:
        json_string (type): Description of parameter `json_string`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    model = model_from_json(json_string)
    return model


def model_visualization(model, config):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    output_dir = os.path.join(config.summary_dir, '.png')

    return plot_model(model=model,
                      to_file=output_dir,
                      show_shapes=True,
                      show_layer_names=True)

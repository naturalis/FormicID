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

import pydot_ng
# import h5py
from keras.models import Model, load_model, model_from_json
from keras.utils.vis_utils import plot_model

import graphviz

# Parameters and settings
###############################################################################
wd = os.getcwd()

# Model utilities
###############################################################################


def save_model(model, filename, output_dir):
    output_model = os.path.join(wd, outputdir, filename)
    model.save(output_model)
    print('The model has been saved and deleted from use.')
    del model


def load_model(filename, input_dir):
    input_model = os.path.join(wd, input_dir, filename)
    model = load_model(input_model)
    print('The model has been loaded.')
    return model


def weights_save(model, filename, output_dir):
    output_weights = os.path.join(wd, outputdir, filename)
    weights_saved = model.save_weights(model)
    print('The weights have been saved.')


def weights_load(model, filename, input_dir):
    input_weights_input = os.path.join(wd, input_dir, filename)
    model.load_weights = load_weights_input(input_model)
    print('The weights have been loaded.')
    return model


def model_summary(model):
    summary = model.summary()
    return summary


def model_config(model):
    config = model.config()
    # Returns a dictionary containing the configuration of the model.
    return config


def model_from_config(config):
    config = model.get_config()
    model = Model.from_config(config)
    return model


def model_architecture(model):
    json_string = model.to_json()
    return json_string


def model_from_architecture(json_string):
    model = model_from_json(json_string)
    return model


def model_visualization(model, config):
    output_dir = os.path.join(config.summary_dir, '.png')

    return plot_model(model=model,
                      to_file=output_dir,
                      show_shapes=True,
                      show_layer_names=True)

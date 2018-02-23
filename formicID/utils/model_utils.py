################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Utilitiies                                  #
#                                    Models                                    #
################################################################################
'''Description:
This file has code utilities for handeling models.
'''
import h5py
# Packages
################################################################################
from keras.models import load_model

wd = os.getcwd()

# Model utilities
################################################################################


def save_model(model, filename, output_dir):
    suffix ='.h5'
    output_model = os.path.join(wd, outputdir, filename, suffix)
    model.save(output_model)
    print('The model has been saved and deleted from use.')
    del model


def load_model(filename, input_dir):
    suffix ='.h5'
    input_model = os.path.join(wd, input_dir, filename, suffix)
    model = load_model(input_model)
    print('The model has been loaded.')
    return model


def weights_save(model, filename, output_dir):
    suffix ='.h5'
    output_weights = os.path.join(wd, outputdir, filename, suffix)
    weights_saved = model.save_weights(model)
    print('The weights have been saved.')


def weights_load(model, filename, input_dir):
    suffix ='.h5'
    input_weights_input = os.path.join(wd, input_dir, filename, suffix)
    model.load_weights = load_weights_input(input_model)
    print('The weights have been loaded.')
    return model


def model_summary(model):
    return model.summary()

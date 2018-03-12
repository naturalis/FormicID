###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Utilitiies                                 #
#                                    Logger                                   #
###############################################################################
'''Description:
Loggers are created in this file. They can be used in training to get feedback
on the models performance.
'''
# Packages
###############################################################################

import os

import keras.backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

from .utils import today_timestr

# Parameters and settings
###############################################################################


# TensorBoard
###############################################################################

class buildTB():
    def __init__(self, model, config):
        """A TensorBoard class object for viewing metrics of the trained model.

        Args:
            model (Keras model instance): The Keras model instance that is
                training.
            config (Bunch object): The JSON configuration Bunch object.

        Returns:
            files: TensorBoard files that can be viewd in the TensorBoard
                dashboard

        """
        self.config = config
        self.model = model
        self.filepath = os.path.join(self.config.summary_dir,
                                     'graphs/logs-{0}'.format(today_timestr))

    def build_tb(self):
        filepath = self.filepath
        model = self.model
        batch_size = self.config.batch_size
        tb = TensorBoard(log_dir=filepath,
                         histogram_freq=0,
                         batch_size=batch_size,
                         write_graph=True,
                         write_images=True)

        tb.set_model(model)

        Callbacks_tb = []
        Callbacks_tb.append(tb)

        return tb

# Model Checkpoint
###############################################################################


class buildMC():

    def __init__(self, config):
        """Class object for saving Model Checkpoints.

        Args:
            config (Bunch object): The JSON configuration Bunch object.

        Returns:
            type: Saves the models at certain checkpoints as `.h5` files.

        """
        self.config = config
        self.filepath = os.path.join(self.config.checkpoint_dir,
                                     'weights_{epoch:02d}-{val_loss:.2f}.hdf5')

    def build_mc(self):
        filepath = self.filepath

        mcp = ModelCheckpoint(filepath=filepath,
                              monitor='val_loss',
                              verbose=0,
                              mode='auto',
                              save_best_only=True,
                              period=1)

        return mcp


# EarlyStopping
###############################################################################
def build_es():
    """For initializing EarlyStopping. This monitors validation loss.

    Returns:
        Training will stop when validation loss is not decreasing anymore.

    """
    es = EarlyStopping(monitor='val_loss',
                       min_delta=0,
                       patience=2,
                       verbose=1,
                       mode='auto')

    return es


# RMSE
###############################################################################

def rmse(y_true,
         y_pred):
    """The root-mean-square-error as a metric to be used in model compilation.

    Args:
        y_true (str): The true label.
        y_pred (str): The predicted label.

    Returns:
        int: the root-mean-square-error.

    """
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

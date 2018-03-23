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

# Standard library imports
import os

# Deeplearning tools imports
import keras.backend as K
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import CSVLogger

from .utils import today_timestr

# Parameters and settings
###############################################################################


# TensorBoard
###############################################################################


def build_tb(
    model,
    config,
    histogram_freq=0,
    write_graph=True,
    write_images=True
):
    """A TensorBoard class object for viewing metrics of the trained model.

    Args:
        model (Keras model instance): The Keras model instance that is
            training.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        files: TensorBoard files that can be by launching the TensorBoard
            dashboard

    """
    filepath = os.path.join(config.summary_dir,
                            'graphs',
                            'logs-{}'.format(today_timestr))
    model = model
    batch_size = config.batch_size
    tb = TensorBoard(
        log_dir=filepath,
        histogram_freq=histogram_freq,
        batch_size=batch_size,
        write_graph=write_graph,
        write_images=write_images
    )

    tb.set_model(model)
    Callbacks_tb = []
    Callbacks_tb.append(tb)

    return tb

# Model Checkpoint
###############################################################################


def build_mc(
    config,
    monitor='val_loss',
    verbose=0,
    mode='auto',
    save_best_only=True,
    period=1
):
    """Callback object for saving Model Checkpoints.

    Args:
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        Saves the models at certain checkpoints as `.h5` files.

    """
    output_dir = config.checkpoint_dir
    filepath = os.path.join(output_dir,
                            'weights_{epoch:02d}-{val_loss:.2f}.hdf5')
    mcp = ModelCheckpoint(
        filepath=filepath,
        monitor=monitor,
        verbose=verbose,
        mode=mode,
        save_best_only=save_best_only,
        period=period
    )

    return mcp


# EarlyStopping
###############################################################################


def build_es(
    monitor='val_loss',
    min_delta=0,
    patience=10,
    verbose=1,
    mode='min'
):
    """For initializing EarlyStopping. This monitors validation loss.

    Returns:
        Training will stop when validation loss is not decreasing anymore.

    """
    es = EarlyStopping(
        monitor=monitor,
        min_delta=min_delta,
        patience=patience,
        verbose=verbose,
        mode=mode
    )

    return es


# Reduce learning rate on plateau
###############################################################################

def build_rlrop(
    monitor='val_loss',
    factor=0.1,
    patience=10,
    verbose=1,
    mode='auto',
    epsilon=1e-4,
    cooldown=0,
    min_lr=0
):
    """Reduce learning rate when a metric has stopped improving.

    Returns:
        Learning rate will decrease when a metric is not improving anymore.

    """
    rlrop = ReduceLROnPlateau(
        monitor=monitor,
        factor=factor,
        patience=patience,
        verbose=verbose,
        mode=mode,
        epsilon=epsilon,
        cooldown=cooldown,
        min_lr=min_lr
    )

    return rlrop

def build_csvl(
    filename,
    config,
    separator=',',
    append=False
):
    output_dir = config.summary_dir
    fname = os.path.join(output_dir, today_timestr + '_' + filename)
    csvlogger = CSVLogger(
        filename=fname,
        separator=separator,
        append=append
    )

    return csvlogger
# RMSE
###############################################################################


def rmse(
    y_true,
    y_pred
):
    """The root-mean-square-error as a metric to be used in model compilation.

    Args:
        y_true (str): The true label.
        y_pred (str): The predicted label.

    Returns:
        int: the root-mean-square-error.

    """
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

# top k categorical accuracy
###############################################################################

def top_k_categorical_accuracy(
    y_true,
    y_pred,
    k=3
):
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k), axis=-1)

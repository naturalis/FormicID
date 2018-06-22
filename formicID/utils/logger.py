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
"""Description:
Loggers are created in this file. They can be used while training to get
feedback on the models performance.
"""

# Packages
###############################################################################

# Standard library imports
import os

# Deeplearning tools imports
import keras.backend as K
from keras.callbacks import CSVLogger
from keras.callbacks import EarlyStopping
from keras.callbacks import History
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import TensorBoard

# Data tools imports
import numpy as np

# Graphical tools imports
import matplotlib.pyplot as plt

from .utils import today_timestr


# TensorBoard
###############################################################################


def build_tb(
    model, config, histogram_freq=0, write_graph=True, write_images=True
):
    """A TensorBoard class object for viewing metrics of the trained model.

    Args:
        model (Keras model instance): The Keras model instance that is
            training.
        config (Bunch object): The JSON configuration Bunch object.
        histogram_freq (int):  Frequency (in epochs) at which to compute
            activation and weight histograms for the layers of the model. If
            set to 0, histograms won't be computed. Validation data (or split)
            must be specified for histogram visualizations. Defaults to True.
        write_graph (Bool): whether to visualize the graph in TensorBoard.
            The log file can become quite large when write_graph is set to
            True. Defaults to True.
        write_images (Bool): Whether to visualize the graph in TensorBoard.
            The log file can become quite large when write_graph is set to
            True. Defaults to True.

    Returns:
        TensorBoard files that can be by launching the TensorBoard dashboard.

    """
    filepath = os.path.join(
        config.summary_dir, "graphs", "logs-{}".format(today_timestr)
    )
    model = model
    batch_size = config.batch_size
    tb = TensorBoard(
        log_dir=filepath,
        histogram_freq=histogram_freq,
        batch_size=batch_size,
        write_graph=write_graph,
        write_images=write_images,
    )

    tb.set_model(model)
    Callbacks_tb = []
    Callbacks_tb.append(tb)

    return tb


# Model Checkpoint
###############################################################################


def build_mc(
    config,
    monitor="val_loss",
    verbose=0,
    mode="auto",
    save_best_only=True,
    period=1,
):
    """Callback object for saving Model Checkpoints. Saves the models at
    certain checkpoints as `.h5` files.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        monitor (str): Quantity to monitor. Defaults to `val_loss`.
        verbose (int): Verbosity mode, 0 or 1. Defaults to 0.
        save_best_only (Bool): If save_best_only=True, the latest best model
            according to the quantity monitored will not be overwritten.
            Defaults to True
        mode (str): One of {auto, min, max}. If save_best_only=True, the
            decision to overwrite the current save file is made based on
            either the maximization or the minimization of the monitored
            quantity. For val_acc, this should be max, for val_loss this
            should be min, etc. In auto mode, the direction is automatically
            inferred from the name of the monitored quantity. Defaults to
            `auto`.
        period (int): Interval (number of epochs) between checkpoints.

    Returns:
        ModelCheckpoint callback

    """
    output_dir = config.checkpoint_dir
    filepath = os.path.join(
        output_dir, "weights_{epoch:02d}-{val_loss:.2f}.hdf5"
    )
    mcp = ModelCheckpoint(
        filepath=filepath,
        monitor=monitor,
        verbose=verbose,
        mode=mode,
        save_best_only=save_best_only,
        period=period,
    )

    return mcp


# EarlyStopping
###############################################################################


def build_es(
    monitor="val_loss", min_delta=0, patience=10, verbose=1, mode="min"
):
    """For initializing EarlyStopping. Training will stop when validation loss
    is not decreasing anymore. This monitors validation loss.

    Args:
        monitor (str): quantity to be monitored. Defaults to val_loss.
        min_delta (int): minimum change in the monitored quantity to qualify
            as an improvement, i.e. an absolute change of less than min_delta,
            will count as no improvement. Defaults to 0.
        patience (int): number of epochs with no improvement after which
            training will be stopped. Defaults to 10.
        verbose (int): verbosity mode. Defaults to 1.
        mode (str): one of {auto, min, max}. In min mode, training will stop
            when the quantity monitored has stopped decreasing; in max mode it
            will stop when the quantity monitored has stopped increasing; in
            auto mode, the direction is automatically inferred from the name
            of the monitored quantity. Defaults to min.

    Returns:
        EarlyStopping callback

    """
    es = EarlyStopping(
        monitor=monitor,
        min_delta=min_delta,
        patience=patience,
        verbose=verbose,
        mode=mode,
    )

    return es


# Reduce learning rate on plateau
###############################################################################


def build_rlrop(
    monitor="val_loss",
    factor=0.1,
    patience=10,
    verbose=1,
    mode="auto",
    min_delta=1e-4,
    cooldown=0,
    min_lr=0,
):
    """Reduce learning rate when a metric has stopped improving.

    Args:
        monitor: quantity to be monitored. Defaults to val_loss.
        factor: factor by which the learning rate will be reduced. new_lr = lr
            * factor. Defaults to 0.1.
        patience: number of epochs with no improvement after which learning
            rate will be reduced. Defaults to 10.
        verbose: int. 0: quiet, 1: update messages. Defaults to 1.
        mode: one of {auto, min, max}. In min mode, lr will be reduced when
            the quantity monitored has stopped decreasing; in max mode it will
            be reduced when the quantity monitored has stopped increasing; in
            auto mode, the direction is automatically inferred from the name
            of the monitored quantity. Defaults to auto.
        min_delta: threshold for measuring the new optimum, to only focus on
            significant changes. Defaults to 1e-4.
        cooldown: number of epochs to wait before resuming normal operation
            after lr has been reduced. Defaults to 0.
        min_lr: lower bound on the learning rate. Defaults to 0.

    Returns:

    """
    rlrop = ReduceLROnPlateau(
        monitor=monitor,
        factor=factor,
        patience=patience,
        verbose=verbose,
        mode=mode,
        min_delta=min_delta,
        cooldown=cooldown,
        min_lr=min_lr,
    )

    return rlrop


# Export metrics to CSVLogger
###############################################################################


def build_csvl(filename, config, separator=",", append=False):
    """Export metrics to a csv file.

    Args:
        filename (str): Name of the csvfile.
        config (Bunch object): The JSON configuration Bunch object.
        separator (str): Set a seperator for the csv file. Defaults to `,`.
        append (Bool): True: append if file exists (useful for continuing
            training). False: overwrite existing file,. Defaults to False.

    Returns:
        CSVLogger callback

    """
    output_dir = config.summary_dir
    fname = os.path.join(output_dir, today_timestr + "_" + filename)
    csvlogger = CSVLogger(filename=fname, separator=separator, append=append)

    return csvlogger


# Plot the history from training - Loss, accuracy, top k accuracy
###############################################################################


def plot_history(history, config, theme="ggplot", save=None):
    """This function will plot the loss, accuracy and top k accuracy after
    training from a Keras Histroy object, with ggplot theme.

    Args:
        history (str): A Keras History object.
        theme (str): Sets the theme for the plot. Defaults to `ggplot`.
        export (str): Path of an file for saving the plot. Defaults to None.

    Returns:
        plot: A plot image made with `matplotlib.pyplot`.

    Raises:
        AssertionError: If the history argument is not a Keras History object.
        ValueError: If `theme` is not one of the available themes.
        TypeError: If `save` is not a valid path.

    """
    if not isinstance(history, History):
        raise AssertionError(
            "The `history` argument: {} is not a Keras "
            "History object.".format(history)
        )

        return

    loss_list = [
        s for s in history.history.keys() if "loss" in s and "val" not in s
    ]
    val_loss_list = [
        s for s in history.history.keys() if "loss" in s and "val" in s
    ]
    acc_list = [
        s
        for s in history.history.keys()
        if "acc" in s and "val" not in s and "top" not in s
    ]
    val_acc_list = [
        s
        for s in history.history.keys()
        if "acc" in s and "val" in s and "top" not in s
    ]
    top_acc_list = [
        s
        for s in history.history.keys()
        if "acc" in s and "val" not in s and "top" in s
    ]
    val_top_acc_list = [
        s
        for s in history.history.keys()
        if "acc" in s and "val" in s and "top" in s
    ]
    if len(loss_list) == 0:
        print("Loss is missing in history")
        return

    epochs = range(1, len(history.history[loss_list[0]]) + 1)
    if theme is not None:
        if theme not in plt.style.available:
            raise ValueError(
                "Theme is not one of {}. {} is not a correct "
                "theme.".format(plt.style.available(), theme)
            )

        else:
            plt.style.use(theme)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    for l in loss_list:
        ax1.plot(
            epochs,
            history.history[l],
            color="b",
            linestyle="-",
            label="Training loss "
            "({0:.5f})".format(history.history["loss"][-1]),
        )
    for l in val_loss_list:
        ax1.plot(
            epochs,
            history.history[l],
            color="b",
            linestyle=":",
            label="Validation loss "
            "({0:.5f})".format(history.history["val_loss"][-1]),
        )
    for l in acc_list:
        ax2.plot(epochs, history.history[l], color="r", linestyle="-")
    for l in val_acc_list:
        ax2.plot(epochs, history.history[l], color="r", linestyle=":")
    for l in top_acc_list:
        ax2.plot(epochs, history.history[l], color="g", linestyle="-")
    for l in val_top_acc_list:
        ax2.plot(epochs, history.history[l], color="g", linestyle=":")
    ax1.plot(
        np.nan,
        color="r",
        linestyle="-",
        label="Training accuracy: "
        "({0:.5f})".format(history.history["acc"][-1]),
    )
    ax1.plot(
        np.nan,
        color="r",
        linestyle=":",
        label="Validation acccuracy: "
        "({0:.5f})".format(history.history["val_acc"][-1]),
    )
    ax1.plot(
        np.nan,
        color="g",
        linestyle="-",
        label="Training top 3 "
        "accuracy: ({0:.5f})".format(
            history.history["top_k_cat_accuracy"][-1]
        ),
    )
    ax1.plot(
        np.nan,
        color="g",
        linestyle=":",
        label="Validation top 3 "
        "acccuracy: ({0:.5f})".format(
            history.history["val_top_k_cat_accuracy"][-1]
        ),
    )
    ax1.legend(loc="best", fancybox=True, framealpha=0.5)
    ax1.grid()
    ax1.set_title(config.exp_name)
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Loss", color="blue")
    ax2.set_ylabel("Accuracy (%)", color="red")
    fig.tight_layout()
    plt.show()
    plt.close("all")
    # TODO: fix saving
    if save is not None:
        try:
            plt.savefig(save)
            print("The confusion matrix has been saved as {}".format(save))
        except TypeError as exc:
            raise ValueError(
                'The `export` argument "{}" is not a valid directory for '
                "saving the figure.".format(export)
            )


# RMSE
###############################################################################


def rmse(y_true, y_pred):
    """The root-mean-square-error as a metric to be used in model compilation.

    Args:
        y_true (str): The true label.
        y_pred (str): The predicted label.

    Returns:
        int: the root-mean-square-error.

    """
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))


# Top k categorical accuracy
###############################################################################


def top_k_cat_accuracy(y_true, y_pred, k=3):
    """Metric for showing the top k categorical accuracy, to be used in model
    compilation.

    Args:
        y_true (str): The true label.
        y_pred (str): The predicted label.
        k (int): Defines the number for a top k accuracy. Defaults to 3.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k), axis=-1)

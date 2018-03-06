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

from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

from .utils import today_timestr

# Parameters and settings
###############################################################################


# TensorBoard
###############################################################################

class buildTB():
    def __init__(self, model, config):
        """Short summary.

        Args:
            model (type): Description of parameter `model`.
            config (type): Description of parameter `config`.

        Returns:
            type: Description of returned object.

        """
        self.config = config
        self.model = model
        self.filepath = os.path.join(self.config.summary_dir,
                                     'graphs/logs-{0}'.format(today_timestr))

    def build_tb(self):
        """Short summary.

        Returns:
            type: Description of returned object.

        """
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
        """Short summary.

        Args:
            config (type): Description of parameter `config`.

        Returns:
            type: Description of returned object.

        """
        self.config = config
        self.filepath = os.path.join(self.config.checkpoint_dir,
                                     'weights_{epoch:02d}-{val_loss:.2f}.hdf5')

    def build_mc(self):
        """Short summary.

        Returns:
            type: Description of returned object.

        """

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
    """Short summary.

    Returns:
        type: Description of returned object.

    """
    es = EarlyStopping(monitor='val_loss',
                       min_delta=0,
                       patience=2,
                       verbose=1,
                       mode='auto')
    # print('Training stopped due to "EarlyStopping"')
    return es

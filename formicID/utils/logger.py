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
class buildTensorBoard():
    def __init__(self, model, config):
        self.config = config
        self.model = model

    def build_tensorboard(self):

        model = self.model
        batch_size = self.config.batch_size
        tb = TensorBoard(log_dir='./graphs/logs/{0}'.format(today_timestr),
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


class buildModelCheckpoint():

    def __init__(self, config):
        self.config = config
        self.filepath = os.path.join(self.config.checkpoint_dir,
                                     'weights_{epoch:02d}-{val_loss:.2f}.hdf5')

    def build_model_checkpoint(self):

        filepath = self.filepath

        mcp = ModelCheckpoint(filepath=filepath,
                              monitor='val_loss',
                              verbose=0,
                              mode='auto',
                              save_best_only=True,
                              period=1)
        mcp.set_model(model)

        Callbacks_mcp = []
        Callbacks_mcp.append(mcp)
        return Callbacks_mcp


# EarlyStopping
###############################################################################
# class buildEarlyStopping():
#     def __init__(self):
#
#     def early_stopping():#
#         Earlystopping(monitor='val_loss',
#                       min_delta=0,
#                       patience=0,
#                       verbose=0,
#                       mode='auto')

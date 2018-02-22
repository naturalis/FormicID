################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Utilitiies                                  #
#                                    Logger                                    #
################################################################################
'''
Description:
A logger for tensorboard is created in this file.

'''
# Packages
################################################################################
from keras.callbacks import TensorBoard
from datetime import datetime
from . import utils

# Parameters and settings
################################################################################


# Callbacks
################################################################################
# class LoggerTensorBoard():
#     def __init__(self, config):
#         self.config = config

def build_tensorboard(model, config=None):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    """
    # TODO (MJABOER):
    # Update batch_size to a universal parameter
    AW_tensorboard = TensorBoard(
        log_dir='./graphs/logs/{0}'.format(today_timestr),
        histogram_freq=3, batch_size=32,
        write_graph=True, write_images=True)
    AW_tensorboard.set_model(model)
    Callbacks_Tensorboard = []
    Callbacks_Tensorboard.append(AW_tensorboard)
    return Callbacks_Tensorboard

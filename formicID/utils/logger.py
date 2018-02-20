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
from keras.callbacks import TensorBoard
from datetime import datetime
# Callbacks
# //////////////////////////////////////////////////////////////////////////////


def build_tensorboard(model):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    """
    AW_tensorboard = TensorBoard(
        log_dir='./graphs/logs/{0}'.format(datetime.now()),
        histogram_freq=0, batch_size=32,
        write_graph=True, write_images=True)
    AW_tensorboard.set_model(model)
    Callbacks_Tensorboard = []
    Callbacks_Tensorboard.append(AW_tensorboard)
    return Callbacks_Tensorboard

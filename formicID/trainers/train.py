################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Trainer                                     #
#                                                                              #
################################################################################
'''
Description:
<placeholder txt>
'''

# Packages
################################################################################

from datetime import datetime

from keras import backend as K
from keras.callbacks import EarlyStopping, TensorBoard
from keras.models import Sequential
from data_loader.data_input import (train_data_generator, train_val_test_split

# from formicID.models.models import (model_densenet169, model_inceptionv3,
#                                     model_resnet50, model_xception)

# TODO (MJABOER):
# loop over batches while training. This is better for the memory.
# Add EarlyStopping

# Parameters and settings
################################################################################
batch_size = 32
epochs = 1


# Training
################################################################################

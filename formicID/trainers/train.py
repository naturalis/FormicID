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

from formicID.data_loader.data_input import (img_load_shottype,
                                             train_data_generator,
                                             train_val_test_split)
from formicID.utils.logger import build_tensorboard
from formicID.models.build import neuralNetwork
# from formicID.models.models import (model_densenet169, model_inceptionv3,
#                                     model_resnet50, model_xception)

# TODO (MJABOER):
    # loop over batches while training. This is better for the memory.
    # Add EarlyStopping

# Parameters and settings
################################################################################
batch_size = 32
epochs = 1


# Initizalizing data
################################################################################
images, labels = img_load_shottype(shottype='h', datadir='2018-02-12-test')

X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
    images=images, labels=labels, test_size=0.1, val_size=0.135)

train_data_gen = train_data_generator(X_train=X_train, Y_train=Y_train, batch_size=batch_size, epochs=epochs)

val_data_gen = train_data_generator(X_val=X_val, Y_val=Y_val, batch_size=batch_size, epochs=epochs)

# Initialize an own desinged neural network
################################################################################
model_formicID = neuralNetwork(
    dropout=0.5,
    input_shape=[120,120,3],
    num_species=97,
    optimizer='Nadam')
model_formicID.build()
model_formicID.compile()


# Training
################################################################################

def main():
    model_formicID.fit_generator(train_data_gen, validation_data=val_data_gen, steps_per_epoch=5, epochs=epochs, callback=build_tensorboard(model_formicID))


if __name__ == '__main__':
    main()
# def trainer(model):
#     """Short summary.
#
#     Args:
#         model (type): Description of parameter `model`.
#
#     Returns:
#         type: Description of returned object.
#
#     """
#     print('Training network...')
#
#     # Generate data using the generator from the image directories.
#     AW_generated_data = train_data_generator(train_data_dir)
#     AW_generated_data_val = validation_data_generator(validation_data_dir)
#
#     AW_model_fit = model.fit_generator(AW_generated_data,
#                                        steps_per_epoch=STEPS_PER_EPOCH,
#                                        epochs=EPOCHS,
#                                        validation_data=AW_generated_data_val,
#                                        validation_steps=10,
#                                        callbacks=build_tensorboard(model))
#     return AW_model_fit

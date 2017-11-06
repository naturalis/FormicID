################################################################################
#                                                                              #
#                        FormicID Network Training                             #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from formicID.formicID_build import *
from formicID.formicID_input import *
from keras.callbacks import TensorBoard
from datetime import datetime

# To Do: store all images in different batches and loop over batches while training. This is better for the memory.

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
train_data_dir = './data/train'
EPOCHS = 5
STEPS_PER_EPOCH = 5

# Training
# //////////////////////////////////////////////////////////////////////////////
AW_model = build_neural_network()
AW_model_comp = compile_neural_network(AW_model)

# AW_model_comp.summary()

AW_generated_data = train_data_generator(train_data_dir)

print(AW_generated_data.class_mode) # shows the class mode
print(AW_generated_data.class_indices) # Shows a dictionary of species and class number
print(AW_generated_data.classes) # shows all classes per specimen
NUM_SPECIES = len(AW_generated_data.class_indices)

# Callbacks
def build_tensorboard(model):
    """
    In order to launch TensorBoard from the terminal, copy between ():
    (tensorboard --logdir="/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/graphs/logs")
    """
    AW_tensorboard = TensorBoard(
        log_dir='./graphs/logs/{0}'.format(datetime.now()),
        histogram_freq=0, batch_size=32,
        write_graph=True, write_images=True)
    AW_tensorboard.set_model(model)
    Callbacks_Tensorboard = []
    Callbacks_Tensorboard.append(AW_tensorboard)
    return Callbacks_Tensorboard


def train_model(model):
    print('Training network...')
    AW_model_fit = model.fit_generator(
        AW_generated_data,
        steps_per_epoch=STEPS_PER_EPOCH,
        epochs=EPOCHS,
        # validation_split=(1/7), # 1/7th of the total (which divides
        # everything in 5:1:1 (train:val:test))
        # validation_data=validation_generator,
        # validation_steps=10,
        callbacks=build_tensorboard(model)
    )
    return AW_model_fit


AW_model_trained = train_model(AW_model_comp)

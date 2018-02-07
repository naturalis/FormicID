################################################################################
#                                                                              #
#                        FormicID Network Training                             #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from keras.callbacks import TensorBoard
from datetime import datetime
from keras import backend as K

from formicID.formicID_input import train_data_generator
from formicID.formicID_input import validation_data_generator

# To Do: store all images in different batches and loop over batches while training. This is better for the memory.

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////


# Callbacks
# //////////////////////////////////////////////////////////////////////////////
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


# Training
# //////////////////////////////////////////////////////////////////////////////

# Print information about the generated test data.
# print('Class mode is:', AW_generated_data.class_mode)  # shows the class mode
# print(AW_generated_data.class_indices) # shows dict of classes and indices
# print(AW_generated_data.classes)  # shows all classes per specimen

#NUM_SPECIES = len(AW_generated_data.class_indices) # the number of species
#print('Number of species found:', NUM_SPECIES, 'species.')

def train_nn(model):
    print('Training network...')

    # Generate data using the generator from the image directories.
    AW_generated_data = train_data_generator(train_data_dir)
    AW_generated_data_val = validation_data_generator(validation_data_dir)

    AW_model_fit = model.fit_generator(AW_generated_data,
                                       steps_per_epoch=STEPS_PER_EPOCH,
                                       epochs=EPOCHS,
                                       validation_data=AW_generated_data_val,
                                       validation_steps=10,
                                       callbacks=build_tensorboard(model))
    return AW_model_fit

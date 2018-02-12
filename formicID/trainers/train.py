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
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from keras.callbacks import TensorBoard
from datetime import datetime
from keras import backend as K

from formicID.models.build import neuralNetwork
from formicID.models.models import model_resnet50, model_xception
from formicID.models.models import model_densenet169, model_inceptionv3
# TODO: loop over batches while training. This is better for the memory.

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////



# Initialize an own desinged neural network
# //////////////////////////////////////////////////////////////////////////////
model_formicID = neuralNetwork(
    dropout=0.5,
    input_shape=[120,120,3],
    num_species=97,
    optimizer='Nadam')
model_formicID.build()
model_formicID_compile()

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


# Training
# //////////////////////////////////////////////////////////////////////////////

# Print information about the generated test data.
# print('Class mode is:', AW_generated_data.class_mode)  # shows the class mode
# print(AW_generated_data.class_indices) # shows dict of classes and indices
# print(AW_generated_data.classes)  # shows all classes per specimen

#NUM_SPECIES = len(AW_generated_data.class_indices) # the number of species
#print('Number of species found:', NUM_SPECIES, 'species.')

def trainer(model):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    """
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

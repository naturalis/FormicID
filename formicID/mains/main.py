################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  main                                #
#                                                                              #
################################################################################
'''
Description:
<placeholder txt>
'''
from keras import __version__ as keras_version
from keras import backend as K

from formicID.formicID_build import neuralNetwork
from formicID.formicID_train import build_tensorboard, train_nn
from formicID.formicID_input import train_data_generator
from formicID.formicID_input import validation_data_generator

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
train_data_dir = './data/train'
validation_data_dir = './data/validation'
EPOCHS = 5
STEPS_PER_EPOCH = 5

num_species = 3  # Todo: implement NUM_SPECIES from _train.py file

img_height, img_width = 120, 148  # input for height and width

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_height, img_width)
else:
    input_shape = (img_height, img_width, 3)

dropout = 0.5

# Running script
# //////////////////////////////////////////////////////////////////////////////

def run():
    """
    Run everything
    """
    AW_nn = neuralNetwork(dropout=dropout,
                          input_shape=input_shape,
                          num_species=num_species,
                          optimizer="Nadam")
    AW_nn = AW_nn.build_neural_network()
    AW_nn_trained = train_nn(AW_nn)
    return AW_nn_trained

if __name__ == '__main__':
    print('Keras version: {}'.format(keras_version))
    run()

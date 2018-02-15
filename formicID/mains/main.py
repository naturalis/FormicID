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
# Packages
################################################################################

from keras import __version__ as keras_version
from keras import backend as K
from keras.utils import multi_gpu_model

from formicID.data_loader.data_input import img_load_shottype
from formicID.models.build import neuralNetwork
from formicID.trainers.train import train_data_gen, val_data_gen
from formicID.utils.logger import build_tensorboardtapp

# Parameters and settings
################################################################################
dropout = 0.5


def main():
    # Initializing the model
    ############################################################################
    model_formicID = neuralNetwork(
        dropout=dropout,
        input_shape=[120, 120, 3],
        num_species=11,
        optimizer='Nadam')
    model_formicID.build()
    model_formicID.compile()
    # multi_gpu_formicID = multi_gpu_model(model_formicID)
    # multi_gpu_formicID = multi_gpu_model(model_formicID, gpus=4)


    # Initializing the data
    ############################################################################
    images, labels = img_load_shottype(shottype='h', datadir='2018-02-12-test')

    X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
        images=images, labels=labels, test_size=0.1, val_size=0.135)

    # Training in batches with iterator
    ##########################################################################
    model_formicID.fit_generator(train_data_gen, validation_data=val_data_gen,
                                 steps_per_epoch=5, epochs=epochs, callback=build_tensorboard(model_formicID))

if __name__ == '__main__':
    print('Keras version: {}'.format(keras.__version__))
    main()

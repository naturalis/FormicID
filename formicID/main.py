################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  main                                        #
#                                                                              #
################################################################################
'''
Description:
<placeholder txt>
'''
# Packages
################################################################################

import os

from keras import __version__ as keras_version
from keras import backend as K
from keras.applications import InceptionV3
from keras.optimizers import SGD, Adam, Nadam, RMSprop
from keras.utils import multi_gpu_model

from data_loader.data_input import (img_height, img_load_shottype, img_width,
                                    train_val_test_split)
from models.build import neuralNetwork
from trainers.train import train_data_generator, val_data_generator
from utils.load_config import process_config
from utils.logger import build_tensorboard
from utils.utils import create_dirs, get_args, wd

# Parameters and settings
################################################################################
batch_size = 16
epochs = 10

# Main
################################################################################
def main():
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print('Missing or invalid arguments.')
        exit(0)

    create_dirs([config.summary_dir, config.checkpoint_dir])

    model = neuralNetwork()
    model.build(model)
    model.compile(model)

    # multi_gpu_formicID = multi_gpu_model(model_formicID)
    # multi_gpu_formicID = multi_gpu_model(model_formicID, gpus=4)

    # Initializing the data
    ############################################################################
    images, labels = img_load_shottype(shottype='h',
                                       datadir='2018-02-12-test')

    X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
        images=images,
        labels=labels,
        test_size=0.1,
        val_size=0.135)

    train_data_gen = train_data_generator(X_train=X_train,
                                          Y_train=Y_train,
                                          batch_size=batch_size,
                                          epochs=epochs)

    val_data_gen = val_data_generator(X_val=X_val,
                                      Y_val=Y_val,
                                      batch_size=batch_size,
                                      epochs=epochs)

    # Training in batches with iterator
    ##########################################################################
    model.fit_generator(train_data_gen,
                        validation_data=val_data_gen,
                        steps_per_epoch=32,
                        epochs=epochs,
                        callbacks=build_tensorboard(model))
    score = model.evaluate(X_test, Y_test, verbose=0)
    print(score)

    prediction = model.predict_classes(X_test, verbose=1)
    print(prediction)


if __name__ == '__main__':
    print('Keras version: {}'.format(keras_version))
    main()

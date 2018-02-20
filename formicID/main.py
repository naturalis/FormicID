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
from keras.layers import (Activation, Conv2D, Dense, Dropout, Flatten,
                          MaxPooling2D)
from keras.models import Sequential  # for creating the model
from keras.models import Model
from keras.optimizers import SGD, Adam, Nadam, RMSprop
from keras.utils import multi_gpu_model

from data_loader.data_input import (img_height, img_load_shottype, img_width,
                                    train_data_generator, train_val_test_split,
                                    val_data_generator)
# from models.models import model_inceptionv3
from utils.logger import build_tensorboard

# Parameters and settings
################################################################################
dropout = 0.5
wd = os.getcwd()
batch_size = 32
epochs = 16


# Main
################################################################################
def main():

    # Initializing the model
    ############################################################################
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(85, 85, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(11))
    model.add(Activation('softmax'))
    print("Model is build succesfully.")

    # if self.optimizer == "SGD":
    #     opt = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
    # if self.optimizer == "RMSprop":
    #     opt = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
    # if self.optimizer == "Nadam":
    #     opt = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08,
    #                 schedule_decay=0.004)

    model.compile(loss='categorical_crossentropy',
                  optimizer=Nadam(lr=0.002,
                                  beta_1=0.9,
                                  beta_2=0.999,
                                  epsilon=1e-08, schedule_decay=0.004)
                  # metrics=['accuracy']
                  )
    print("Model is compiled succesfully.")
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

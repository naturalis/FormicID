################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                      main                                    #
#                                                                              #
################################################################################
'''Description:
This is were it all happens. This file loads the data, initializes the model
and trains the model. Log files are made and a prediction can be made for the
test set.
'''
# Packages
################################################################################

from keras import __version__ as keras_version
from keras import backend as K
from keras.applications.inception_v3 import InceptionV3  # Inception based
from keras.optimizers import SGD, Adam, Nadam, RMSprop
from keras.utils import multi_gpu_model

# Antweb utils
from AntWeb.AW2_to_json import urls_to_json
from AntWeb.json_to_csv import batch_json_to_csv
# Data loader
from data_loader.data_input import (img_height, img_load_shottype, img_width,
                                    train_val_test_split)
# Data scraper
from data_scraper.scrape import image_scraper
# Models
# from models.build import neuralNetwork
# from models.models import modelLoad
# Trainer
from trainers.train import train_data_generator, val_data_generator
# Utilities
from utils.img import save_augmentation
from utils.load_config import process_config
from utils.logger import build_tensorboard
from utils.utils import create_dirs, get_args, today_timestr, todaystr, wd

# Parameters and settings
################################################################################
batch_size = 16
epochs = 32

# Main
################################################################################


def main():
    # Get args
    ############################################################################
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print('Missing or invalid arguments.')
        exit(0)

    # Creating urls and export to json files
    ############################################################################
    # urls_to_json(csv_file='2018-01-09-db-Top101imagedspecies.csv',
    #              input_dir='data',
    #              output_dir='test',
    #              offset_set=0,
    #              limit_set=12000)

    # downloading from json files to a scrape ready csv file
    ############################################################################
    # batch_json_to_csv(
    #     input_dir='2018-02-23-test',
    #     output_dir='2018-02-23-test',
    #     csvname='csv_images')

    # scrape the images from the csv file and name accordingly
    ############################################################################
    # image_scraper(csvfile='csv_images.csv',
    #               input_dir='2018-02-23-test',
    #               start=0,
    #               end=5000,
    #               dir_out_name='images',
    #               update=True)

    # create experiment related directories
    ############################################################################
    create_dirs([config.summary_dir, config.checkpoint_dir])

    # Initialize the model
    ############################################################################
    # model = modelLoad(config=config)
    model = InceptionV3(include_top=True, weights=None,
                        input_tensor=None, input_shape=(140, 140, 3), pooling='avg')

    model.compile(loss='categorical_crossentropy',
                  optimizer=Nadam(lr=0.002,
                                  beta_1=0.9,
                                  beta_2=0.999,
                                  epsilon=1e-08,
                                  schedule_decay=0.004))
    print('The model is loaded and compiled.')

    # model = neuralNetwork()
    # model.build(model)
    # model.compile(model)

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

    # save_augmentation(image='camponotus_auropubens_casent0101126_d.jpg',
    #                   test_dir='data/2018-02-12-test',
    #                   input_dir='images/dorsal/camponotus_auropubens/')

    print('Data is loaded and generated.')

    # Training in batches with iterator
    #########################################################################
    # model.fit_generator(train_data_gen,
    #                     validation_data=val_data_gen,
    #                     steps_per_epoch=32,
    #                     epochs=epochs,
    #                     callbacks=build_tensorboard(model))
    #
    # score = model.evaluate(X_test, Y_test, verbose=0)
    # print(score)
    #
    # prediction = model.predict_classes(X_test, verbose=1)
    # print(prediction)


if __name__ == '__main__':
    print('Keras version: {}'.format(keras_version))
    main()

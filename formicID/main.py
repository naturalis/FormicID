###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                      main                                   #
#                                                                             #
###############################################################################
'''Description:
This is were it all happens. This file loads the data, initializes the model
and trains the model. Log files are made and a prediction can be made for the
test set.
'''
# Packages
###############################################################################

import logging
import os

import tensorflow as tf
from keras import __version__ as keras_version
from keras import backend as K

from AntWeb.AW2_to_json import urls_to_json
from AntWeb.json_to_csv import batch_json_to_csv
from data_loader.data_input import load_data
from data_scraper.scrape import image_scraper
from models.models import compile_model, load_model
from trainers.train import trainer
from utils.img import save_augmentation, show_multi_img
from utils.load_config import process_config
from utils.logger import build_es, buildMC, buildTB
from utils.model_utils import (make_multi_gpu, model_summary,
                               model_visualization)
from utils.utils import create_dirs, get_args

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# 0 = all logs, 1 = info, 2 = warnings, 3 = error

# Parameters and settings
###############################################################################


# Main
###############################################################################


def main():

    print('Keras version: {}'.format(keras_version))

    # logging.basicConfig(filename='loggerfile.log', level=logging.INFO)

    # Get args
    ###########################################################################
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print('Missing or invalid arguments.')
        exit(0)

    # Creating urls and export to json files
    ###########################################################################
    urls_to_json(csv_file='testgenusspecies.csv',
                 input_dir='data',
                 output_dir='test5sp',
                 offset_set=0,
                 limit_set=12000)

    # Downloading from json files to a scrape ready csv file
    ###########################################################################
    batch_json_to_csv(
        input_dir='2018-03-06-test5sp',
        output_dir='2018-03-06-test5sp',
        csvname='csv_images.csv')

    # Scrape the images from the csv file and name accordingly
    ###########################################################################
    image_scraper(csvfile='csv_images.csv',
                  input_dir='2018-03-06-test5sp',
                  start=0,
                  end=1491,
                  dir_out_name='images',
                  update=True)

    # create experiment related directories
    ###########################################################################
    create_dirs([config.summary_dir, config.checkpoint_dir])

    # Initializing the data
    ###########################################################################
    X_train, Y_train, X_val, Y_val, X_test, Y_test, num_species = load_data(
        datadir='2018-03-06-test5sp',
        config=config,
        shottype='h')

    print('Data is loaded, split and put in generators.')
    # num_species = 5

    # show_multi_img(X_train=X_train, Y_train=Y_train)

    # save_augmentation(
    #     image='data/2018-03-06-test5sp/images/head/pheidole_megacephala/pheidole_megacephala_casent0059654_h.jpg',
    #     config=config)

    # Initialize the model
    ###########################################################################
    model_formicID = load_model(config=config,
                                num_classes=num_species,
                                base_model='InceptionV3',
                                optimizer='Nadam')

    # model_formicID = make_multi_gpu(model=model_formicID,
    #                                 gpus=4)

    model_formicID = compile_model(model=model_formicID,
                                   config=config)

    print('type ', model_formicID)
    # print(model_summary(model_formicID))
    # model_visualization(model=model_formicID,
    #                     config=config)

    # Initialize logger
    ###########################################################################
    logger = [buildMC(config=config).build_mc(),
              buildTB(model=model_formicID, config=config).build_tb(),
              build_es()]

    # Training in batches with iterator
    ###########################################################################
    trainer(model=model_formicID,
            X_train=X_train,
            Y_train=Y_train,
            X_val=X_val,
            Y_val=Y_val,
            callbacks=logger,
            config=config)

    # Evaluation
    ###########################################################################
    # score = model.evaluate(X_test, Y_test, verbose=0)
    # print(score)

    # Testing
    ###########################################################################
    # prediction = model.predict_classes(X_test, verbose=1)
    # print(prediction)

    K.clear_session()


if __name__ == '__main__':
    main()

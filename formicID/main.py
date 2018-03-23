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

# Standard library imports
import logging
import os

# Deeplearning tools imports
import tensorflow as tf
from keras import __version__ as keras_version
from keras import backend as K

# FormicID imports
from AntWeb.AW2_to_json import urls_to_json
from AntWeb.json_to_csv import batch_json_to_csv
from data_loader.data_input import make_image_path_csv
from data_loader.data_input import split_in_directory
from data_scraper.scrape import image_scraper
from models.models import compile_model
from models.models import load_model
from testers.tester import model_evaluate
from trainers.train import trainer_csv
from trainers.train import trainer_dir
from utils.load_config import process_config
from utils.logger import build_es
from utils.logger import build_rlrop
from utils.logger import build_mc
from utils.logger import build_tb
from utils.logger import build_csvl
from utils.model_utils import make_multi_gpu
from utils.utils import create_dirs
from utils.utils import get_args

# Parameters and settings
###############################################################################
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# To disable the tf warning for compiling in SEE4.2
# 0 = all logs, 1 = info, 2 = warnings, 3 = error


# Main
###############################################################################


def main():
    sess = tf.Session()
    K.set_session(sess)
    # Logging
    ###########################################################################
    logging.basicConfig(
        filename='loggerfile.log',
        format='[%(asctime)s] - [%(levelname)s]: %(message)s',
        filemode='w',
        level=logging.DEBUG
    )
    logging.info('Keras version: {}'.format(keras_version))
    # Get args
    ###########################################################################
    try:
        args = get_args()
        config = process_config(args.config)
    except:
        logging.error('Missing or invalid arguments.')
        exit(0)

    # Creating a dataset
    ###########################################################################
    # urls_to_json(
    #     csv_file='testgenusspecies.csv',
    #     input_dir='data',
    #     output_dir='5sp_200limit',
    #     offset_set=0,
    #     limit_set=200
    # )
    # batch_json_to_csv(
    #     input_dir='2018-03-21-5sp_200limit',
    #     output_dir='2018-03-21-5sp_200limit',
    #     quality='low',
    #     csvname='image_urls.csv'
    # )
    # image_scraper(
    #     csvfile='image_urls.csv',
    #     input_dir='2018-03-21-5sp_200limit',
    #     # start=0,
    #     # end=1491,
    #     dir_out_name='images',
    #     update=False
    # )
    # make_image_path_csv(
    #     data_dir='2018-03-21-5sp_200limit'
    # )
    # create experiment related directories
    ###########################################################################
    create_dirs(
        [config.summary_dir,
         config.checkpoint_dir]
    )
    # Initializing the data
    ###########################################################################
    # split_in_directory(
    #     data_dir='2018-03-16-testall',
    #     shottype='dorsal',
    #     test_split=0.1,
    #     val_split=0.2
    # )
    # split_in_directory(
    #     data_dir='2018-03-16-testall',
    #     shottype='head',
    #     test_split=0.1,
    #     val_split=0.2
    # )
    # split_in_directory(
    #     data_dir='2018-03-16-testall',
    #     shottype='profile',
    #     test_split=0.1,
    #     val_split=0.2
    # )
    num_species = 97
    # Initialize the model
    ###########################################################################
    model_formicID = load_model(
        config=config,
        num_classes=num_species,
        base_model='InceptionV3'
    )
    model_formicID = compile_model(
        model=model_formicID,
        config=config
    )
    # Initialize logger
    ###########################################################################
    logger = [
        build_mc(
            config=config,
            monitor='val_loss',
            verbose=0,
            mode='auto',
            save_best_only=True,
            period=1
        ),
        build_rlrop(
            monitor='val_loss',
            factor=0.1,
            patience=10,
            verbose=1,
            mode='auto',
            epsilon=1e-4,
            cooldown=0,
            min_lr=0
        ),
        build_es(
            monitor='val_loss',
            min_delta=0,
            patience=25,
            verbose=1,
            mode='min'
        ),
        build_tb(
            model=model_formicID,
            config=config,
            histogram_freq=0,
            write_graph=True,
            write_images=True
        ),
        build_csvl(
            filename='log.csv',
            config=config,
            separator=',',
            append=False)
    ]
    # Training in batches with iterator
    ###########################################################################
    # trainer(
    #     model=model_formicID,
    #     X_train=X_train,
    #     Y_train=Y_train,
    #     X_val=X_val,
    #     Y_val=Y_val,
    #     callbacks=logger,
    #     config=config
    # )
    trainer_dir(
        model=model_formicID,
        data_dir='2018-03-16-testall',
        shottype='head',
        config=config,
        callbacks=logger
    )
    # trainer_csv(
    #     model=model_formicID,
    #     csv='data/2018-03-21-5sp_200limit/image_path.csv',
    #     shottype='head',
    #     config=config,
    #     callbacks=None
    # )
    # Evaluation
    ###########################################################################
    # score = model_evaluate(model_formicID, X_test, Y_test)

    # Testing
    ###########################################################################
    # prediction = model_formicID.predict_classes(
    #     X_test,
    #     verbose=1
    # )
    # logging.info(prediction)

    K.clear_session()


if __name__ == '__main__':
    main()

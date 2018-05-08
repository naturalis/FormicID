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
"""Description:
This is were it all happens. This file loads the data, initializes the model
and trains the model. Log files are made and a prediction can be made for the
test set.
"""
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
from data_loader.data_input import split_in_directory
from data_scraper.scrape import get_dataset
from models.models import compile_model
from models.models import load_model
from testers.tester import evaluator
from testers.tester import plot_confusion_matrix
from testers.tester import predict_image
from testers.tester import predictor
from trainers.train import trainer_csv
from trainers.train import trainer_dir
from utils.img import save_augmentation
from utils.load_config import process_config
from utils.logger import build_csvl
from utils.logger import build_es
from utils.logger import build_mc
from utils.logger import build_rlrop
from utils.logger import build_tb
from utils.logger import plot_history
from utils.model_utils import weights_load
from utils.utils import create_dirs
from utils.utils import get_args
from utils.utils import today_time_clean

# Parameters and settings
###############################################################################
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
# To disable the tf warning for compiling in SEE4.2
# 0 = all logs, 1 = info, 2 = warnings, 3 = error


# Main
###############################################################################


def main():
    # Arguments
    ###########################################################################
    try:
        args = get_args()
        config = process_config(args.config)
    except:
        logging.error("Missing or invalid arguments.")
        exit(0)

    # Logging
    ###########################################################################
    logging.basicConfig(
        filename=os.path.join("logs", config.exp_name + ".log"),
        format="[%(asctime)s] - [%(levelname)s]: %(message)s",
        filemode="w",
        level=logging.DEBUG,
    )
    logging.info("Logging started on: {}".format(today_time_clean))
    logging.info("Keras version: {}".format(keras_version))

    # Session
    ###########################################################################
    sess = tf.Session()
    K.set_session(sess)

    # Creating a dataset
    ###########################################################################
    # get_dataset(
    #     input="testall.csv",
    #     n_jsonfiles=100,
    #     config=config,
    #     shottypes="h",
    #     quality="thumbview",
    #     update=True,
    #     offset_set=0,
    #     limit_set=9999,
    # )

    # create experiment related directories
    ###########################################################################
    create_dirs([config.summary_dir, config.checkpoint_dir])

    # Initializing the data
    ###########################################################################
    split_in_directory(config=config)

    # Augmentation handeling
    ###########################################################################
    # save_augmentation(
    #     image="data/top97species_Qmed/bothroponera_cambouei_blf0561(26)-1_h.jpg",
    #     config=config,
    #     show=True,
    # )

    # Initialize the model
    ###########################################################################
    model_formicID = load_model(config=config)
    model_formicID = compile_model(model=model_formicID, config=config)
    # model_formicID = weights_load(
    #     model=model_formicID,
    #     weights="experiments\T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4\checkpoint\weights_64-1.21.hdf5",
    # )

    # Initialize logger
    ###########################################################################
    logger = [
        build_mc(
            config=config,
            monitor="val_loss",
            verbose=0,
            mode="min",
            save_best_only=True,
            period=1,
        ),
        build_rlrop(
            monitor="val_loss",
            factor=0.1,
            patience=25,
            verbose=1,
            mode="min",
            epsilon=1e-4,
            cooldown=0,
            min_lr=0,
        ),
        build_es(
            monitor="val_loss", min_delta=0, patience=50, verbose=1, mode="min"
        ),
        build_tb(
            model=model_formicID,
            config=config,
            histogram_freq=0,
            write_graph=True,
            write_images=True,
        ),
        build_csvl(
            filename="metricslog.csv",
            config=config,
            separator=",",
            append=False,
        ),
    ]

    # Training in batches with iterator
    ###########################################################################
    history = trainer_dir(
        model=model_formicID, config=config, callbacks=logger
    )
    # trainer_csv(
    #     model=model_formicID,
    #     csv="data/top5species_Qlow/image_path.csv",
    #     shottype="head",
    #     config=config,
    #     callbacks=None,
    # )

    # Evaluation
    ###########################################################################
    plot_history(history=history, theme="ggplot", save=None)
    evaluator(model=model_formicID, config=config)

    # Testing
    ###########################################################################
    Y_true, Y_pred, labels, species_dict = predictor(
        model=model_formicID, config=config, plot=True, n_img=10, n_cols=3
    )
    plot_confusion_matrix(
        Y_pred=Y_pred,
        Y_true=Y_true,
        target_names=labels,
        title="Confusion matrix",
        cmap="viridis",
        normalize=True,
        scores=True,
        score_size=8,
        save="confusion_matrix_test.png",
    )
    predict_image(
        model=model_formicID,
        url="https://upload.wikimedia.org/wikipedia/commons/f/fd/Camponotus_atriceps_casent0173392_head_1.jpg",
        species_dict=species_dict,
    )

    # Footer
    ###########################################################################
    K.clear_session()
    logging.info("Logging ended on: {}".format(today_time_clean))


if __name__ == "__main__":
    main()

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

from AntWeb.AW2_to_json import urls_to_json
from AntWeb.json_to_csv import batch_json_to_csv
from data_loader.data_input import img_load_shottype, train_val_test_split
from data_scraper.scrape import image_scraper
from models.models import model_inceptionv3
# from models.models import modelLoad
from trainers.train import train_data_generator, val_data_generator
from utils.img import save_augmentation
from utils.load_config import process_config
from utils.logger import buildTensorBoard, buildModelCheckpoint
from utils.utils import create_dirs, get_args, today_timestr, todaystr, wd

# Parameters and settings
################################################################################
batch_size = 6
epochs = 2

# Main
################################################################################


def main():

    print('Keras version: {}'.format(keras_version))

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
    
    model = model_inceptionv3
    model_inceptionv3.compile(loss='categorical_crossentropy',
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

    # print('X_train shape: ', X_train.shape)
    # print('Y_train shape: ', Y_train.shape)

    train_data_gen = train_data_generator(X_train=X_train,
                                          Y_train=Y_train,
                                          batch_size=batch_size,
                                          epochs=epochs)

    val_data_gen = val_data_generator(X_val=X_val,
                                      Y_val=Y_val,
                                      batch_size=batch_size,
                                      epochs=epochs)



    # save_augmentation(image='anochetus_madagascarensis_casent0101674_h.jpg',
    #                   test_dir='data/2018-02-12-test',
    #                   input_dir='images/head/anochetus_madagascarensis')
    #
    print('Data is loaded, split and put in generators.')

    # Training in batches with iterator
    #########################################################################


    # logger = [buildModelCheckpoint(config=config),
    #           buildTensorBoard(model=model_inceptionv3,
    #                            config=config)]
    #
    #
    #
    # model.fit_generator(train_data_gen,
    #                     validation_data=val_data_gen,
    #                     steps_per_epoch=3,
    #                     epochs=epochs,
    #                     callbacks=logger)
    #
    # score = model.evaluate(X_test, Y_test, verbose=0)
    # print(score)
    #
    # prediction = model.predict_classes(X_test, verbose=1)
    # print(prediction)


if __name__ == '__main__':
    main()

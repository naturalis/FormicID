###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  data_input                                 #
###############################################################################
'''Description:
`These scripts can import data from image files in folders and split them in
different subsets. If data is downloaded using the scraper script the files
should be in a correct folder structure (divided per shottype and species). The
script also encodes labels and preprocesses the images into the right format
for tensorflow ([-1, 1] range) and in RGB. With `train_val_test_split` the
data can be split in 3 subsets: Training, validation and test sets. You can
set the splits. Imags are always in (width, height, channel) format. Only the
Keras `load_img()` function reads a target size in (height, width).

The files should be structured as follows:

```
    directory_name/
        head/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...
        dorsal/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...
```

'''
# Packages
###############################################################################

import logging
import os
import random
import shutil

import numpy as np
import pandas as pd
from keras import backend as K
from keras.preprocessing.image import img_to_array, load_img
from keras.utils import normalize, to_categorical
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

from utils.utils import wd

# Parameters and settings
###############################################################################


# Create image loading csvfile
###############################################################################


def image_path_csv_input(data_dir):
    data_dir = os.path.join('data', data_dir)
    image_dir = os.path.join(data_dir, 'images')
    path_col = []
    shottype_col = []
    species_col = []
    identifier_col = []
    for shottype in tqdm(os.listdir(image_dir)):
        for species in tqdm(os.listdir(os.path.join(image_dir, shottype))):
            for image in tqdm(os.listdir(os.path.join(image_dir,
                                                      shottype,
                                                      species))):
                if image.endswith('.jpg'):
                    identifier = os.path.split(image)[1].split('_')[2]
                    image = os.path.join(image_dir, shottype, species, image)
                    path_col.append(image)
                    shottype_col.append(shottype)
                    species_col.append(species)
                    identifier_col.append(identifier)
    data = list(zip(identifier_col, species_col, shottype_col, path_col))
    df = pd.DataFrame(data,
                      columns=['Identifier',
                               'Species',
                               'Shottype',
                               'path'])
    output_csv = os.path.join(data_dir, 'image_path.csv')
    df.to_csv(path_or_buf=output_csv,
              header=True,
              index=False,
              sep=",")


# Return the image dimensions according to a choosen model
###############################################################################


def _image_size(config):
    """Function that returns the correct input size according to the choosen
    model.

    Args:
        config (JSON object): The JSON configuration file.

    Returns:
        int: returns an integer of the image width and height.

    Raises:
        AssertionError: When an unvalid model is set.

    """
    model = config.model
    if model not in ['InceptionV3',
                     'Xception',
                     'Resnet50',
                     'DenseNet169',
                     'Build']:
        raise AssertionError(
            'Model should be one of `InceptionV3`, `Xception`, `Resnet50` or',
            '`DenseNet169` or `Build`. Please set a correct model in the '
            'config file. The set model: {} is incorrect'.format(model))
    if model == 'InceptionV3':
        img_width, img_height = 299, 299
    if model == 'Xception':
        img_width, img_height = 299, 299
    if model == 'ResNet50':
        img_width, img_height = 224, 224
    if model == 'DenseNet169':
        img_width, img_height = 224, 244
    logging.info('Choosen model: {}. '
                 'Img width: {}. '
                 'Img height: {}.'.format(model, img_width, img_height))
    return img_width, img_height


# Load the images providing a shottype
###############################################################################


def img_load_shottype(shottype,
                      datadir,
                      img_size=(None, None)):
    """This function loads images from a directory for which the shottype is
    given. Normalization happens in the `ImageDataGenerator`.

    Args:
        shottype (str): Specifie the shottype using the following options:
            - `h` (head),
            - `d` (dorsal)
            - `p` (profile)
        datadir (str): The data directory that contains the `images` folder.
        img_size (int): The image width and height, this will be inferred from
            the choosen model, set by the configuration file.

    Returns:
        images (array): images as numpy 4D arrays (batches, width, height,
        channels) (RGB).
        labels (array): labels as numpy 2d arrays (batches, labels).

    Raises:
        ValueError: If the shottype is not one of `h`, `d` or `p`.

    """
    img_width, img_height = img_size
    logging.info('The dataset is {}'.format(datadir))
    data_dir = os.path.join(wd,
                            'data',
                            datadir,
                            'images')
    if shottype not in ['h', 'd', 'p']:
        raise ValueError('Shottype should be either `h`, `d` or `p`.')
    if shottype == 'h':
        data_dir = os.path.join(data_dir,
                                'head')
    if shottype == 'd':
        data_dir = os.path.join(data_dir,
                                'dorsal')
    if shottype == 'p':
        data_dir = os.path.join(data_dir,
                                'profile')
    images = []
    labels = []
    for _, dirs, _ in os.walk(data_dir):
        num_species = len(dirs)
        break
    logging.info('Reading images from "{}"'.format(data_dir))
    for species in tqdm(os.listdir(data_dir),
                        desc='Reading folders',
                        unit='species'):
        for image in tqdm(os.listdir(os.path.join(data_dir,
                                                  species)),
                          desc='Loading {}'.format(species),
                          unit='images'):
            if '.jpg' in image:
                if img_height != None and img_width != None:
                    img = load_img(path=os.path.join(data_dir,
                                                     species,
                                                     image),
                                   grayscale=False,
                                   # Keras load_img takes H, W
                                   # PIL image instance uses W, H
                                   target_size=(img_height, img_width),
                                   interpolation='nearest')
                    imgs = img_to_array(img,
                                        data_format='channels_last')
                    images = np.append(images,
                                       imgs)
                else:
                    img = load_img(path=os.path.join(data_dir,
                                                     species,
                                                     image),
                                   grayscale=False)
                    imgs = img_to_array(img,
                                        data_format='channels_last')
                    images.append(imgs)
            label = species
            labels = np.append(labels, label)
    images = np.reshape(images, (-1, img_width, img_height, 3))
    # Cast np array to keras default float type ('float32')
    images = K.cast_to_floatx(images)
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels = to_categorical(labels,
                            num_classes=num_species)
    labels = K.cast_to_floatx(labels)
    logging.debug('Number of species: {}'.format(num_species))
    logging.debug('Images shape (N, W, H, C): {}'.format(images.shape))
    logging.debug('Images dtype: {}'.format(images.dtype))
    logging.debug('Labels shape (N, L): {}'.format(labels.shape))
    logging.debug('Labels dtype: {}'.format(labels.dtype))
    print('\n')  # Because text after tqdm does not escape on a new line.
    return images, labels, num_species


# Training, validation and test split
###############################################################################


def train_val_test_split(images,
                         labels,
                         seed,
                         test_size=0.1,
                         val_size=0.135):
    """Split the data in a training, validation and test set. You can specify
    the test size and validation size. The set will be split in to (test -
    (training + validation)) first, and then (training - validation) will be
    split.

    Args:
        images (array): all images as 4d array.
        labels (array): all labels in relation to the images.
        test_size (float): size of the training set. Default is `0.1`, which
            is 10 percent of the total set.
        val_size (float): size of the validation set. Default is set to
            `0.135`, which is is around 15 percent of the total input set.

    Returns:
        arrays: Returns the split arrays of images and labels for training,
            validation and testing.

    Raise:
        TypeError: When `test_size` or `val_size` is not an integer.

    """
    try:
        sss = StratifiedShuffleSplit(n_splits=1,
                                     test_size=test_size,
                                     random_state=seed)
        sss.get_n_splits(images,
                         labels)
        for train_index, test_index in sss.split(images,
                                                 labels):
            logging.debug('Test index (10%%): {}'.format(test_index))
            X_train, X_test = images[train_index], images[test_index]
            Y_train, Y_test = labels[train_index], labels[test_index]
    except TypeError:
        logging.error('`test_size` is not an integer.')
    try:
        sss = StratifiedShuffleSplit(n_splits=1,
                                     test_size=val_size,
                                     random_state=seed)
        sss.get_n_splits(X_train,
                         Y_train)
        for train_index, val_index in sss.split(X_train,
                                                Y_train):
            logging.debug('Training index (~75%%): {}'.format(train_index))
            logging.debug('Validation index (~15%%): {}'.format(val_index))
            X_train, X_val = X_train[train_index], X_train[val_index]
            Y_train, Y_val = Y_train[train_index], Y_train[val_index]
    except TypeError:
        logging.error('`val_size` is not an integer.')
    nb_specimens = len(X_test) + len(X_train) + len(X_val)
    logging.debug('Total number of images: {}'.format(nb_specimens))
    logging.debug('Number of X_test: {}'.format(len(X_test)))
    logging.debug('Number of X_train: {}'.format(len(X_train)))
    logging.debug('Number of X_val: {}'.format(len(X_val)))
    return X_train, Y_train, X_val, Y_val, X_test, Y_test


# Split training/validation/test in folder
###############################################################################

def split_in_directory(data_dir,
                       shottype='head',
                       test_split=0.1,
                       val_split=0.2):
    """Split the image files for all species into subfolders for a training,
    validation and test set.

    Args:
        data_dir (str): Directory that holds the shottype folders with species
            and images.
        shottype (str): The shottype folder. Defaults to 'head'.
        test_split (float): Percentage of images for the test set. Defaults to
            0.1.
        val_split (float): Percentage of images for the validation set.
            Defaults to 0.2.

    """
    val_split = val_split + test_split
    input_dir = os.path.join(wd, 'data', data_dir, 'images', shottype)
    dirs_split = ['1-training', '2-validation', '3-test']
    for dir in dirs_split:
        if not os.path.exists(os.path.join(input_dir, dir)):
            os.makedirs(os.path.join(input_dir, dir))
    for dir in dirs_split:
        for species in os.listdir(input_dir):
            if species in dirs_split:
                continue
            if not os.path.exists(os.path.join(input_dir, dir, species)):
                os.makedirs(os.path.join(input_dir, dir, species))
    train_dir = os.path.join(input_dir, dirs_split[0])
    val_dir = os.path.join(input_dir, dirs_split[1])
    test_dir = os.path.join(input_dir, dirs_split[2])
    for species in tqdm(os.listdir(input_dir)):
        if species in dirs_split:
            continue
        nb_images = len(os.listdir(os.path.join(input_dir, species)))
        # print(nb_images)
        image_files = os.listdir(os.path.join(input_dir, species))
        shuffled = image_files[:]
        random.shuffle(shuffled)
        num1 = round(len(shuffled) * test_split)
        num2 = round(len(shuffled) * val_split)
        to_test, to_val, to_train = shuffled[:num1], shuffled[num1:num2], \
            shuffled[num2:]
        for image in os.listdir(os.path.join(input_dir, species)):
            if image.endswith('.jpg'):
                for img in to_test:
                    shutil.copy2(os.path.join(input_dir, species, img),
                                 os.path.join(test_dir, species, img))
                for img in to_val:
                    shutil.copy(os.path.join(input_dir, species, img),
                                os.path.join(val_dir, species, img))
                for img in to_train:
                    shutil.copy2(os.path.join(input_dir, species, img),
                                 os.path.join(train_dir, species, img))


# Stitching it all together
###############################################################################


def load_data(datadir, config, shottype='h'):
    """Combining the loading of images and labels together with the splitting
    function.

    Args:
        datadir (str): The data directory that contains the `images` folder.
        config (JSON object): the JSON configuration file.
        shottype (str): Specifie the shottype using the following options:
            - `h` (head),
            - `d` (dorsal)
            - `p` (profile).
            Defaults to `h`.

    Returns:
        arrays: Arrays of images and labels for training, validation and
            testing.

    """
    seed = config.seed
    img_width, img_height = _image_size(config=config)
    images, labels, num_species = img_load_shottype(shottype=shottype,
                                                    datadir=datadir,
                                                    img_size=(img_width,
                                                              img_height))
    X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
        images=images,
        labels=labels,
        seed=seed,
        test_size=0.1,
        val_size=0.135)
    logging.info('Data is loaded, split and put in generators.')

    return X_train, Y_train, X_val, Y_val, X_test, Y_test, num_species

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
`These scripts can import data from files in folders and split them in
different subsets. If data is downloaded using the scraper script the files
should be in a correct folder structure (divided per shottype and species). The
script also encodes labels and preprocesses the images into the right format
for tensorflow ([-1, 1] range) and in RGB. With `train_val_test_split` the
data can be split in 3 subsets: Training, validation and test sets. You can
set the splits.

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

import os

import numpy as np
from keras import backend as K
from keras.preprocessing.image import img_to_array, load_img
from keras.utils import normalize, to_categorical
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

from utils.utils import wd

# Parameters and settings
###############################################################################
seed = 1337


# Load images
###############################################################################
def image_size(config):
    """Function that returns the correct input size for the choosen model.

    Args:
        config (JSON): The JSON configuration file.

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
            '`DenseNet169` or `Build`. Please set a correct model.')

    if model == 'InceptionV3':
        img_width, img_height = 299, 299

    if model == 'Xception':
        img_width, img_height = 299, 299

    if model == 'ResNet50':
        img_width, img_height = 224, 224

    if model == 'DenseNet169':
        img_width, img_height = 224, 244

    print('Img height: {0}. Img width: {1}. Set by choosen model: {2}'.format(img_height, img_width, model))

    return img_width, img_height


def img_load_shottype(shottype,
                      datadir,
                      img_height=None,
                      img_width=None):
    """This function loads images from a directory for which the shottype is
    given. Normalization happens in the `ImageDataGenerator`.

    Args:
        shottype (str): Specifie the shottype using the following options:
            - `h` (head),
            - `d` (dorsal)
            - `p` (profile)
        datadir (str): The data directory that contains the `images` folder.
        config (JSON): The JSON configuration file.

    Returns:
        images (array): images as numpy 4D arrays (batches, height, width,
        channels) (RGB).
        labels (array): labels as numpy 2d arrays (batches, labels).

    """
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
    num_species = len(next(os.walk(data_dir))[1])

    print('Reading images from "{}"'.format(data_dir))

    for species in tqdm(os.listdir(data_dir),
                        desc='Reading folders',
                        unit='species'):
        for image in tqdm(os.listdir(os.path.join(data_dir,
                                                  species)),
                          desc='Loading {}'.format(species),
                          unit='images'):
            if '.jpg' in image:
                img = load_img(path=os.path.join(data_dir,
                                                 species,
                                                 image),
                               grayscale=False,
                               target_size=(img_height,
                                            img_width),
                               interpolation='nearest')
                imgs = img_to_array(img,
                                    data_format='channels_last')
                images = np.append(images,
                                   imgs)

            label = species
            labels = np.append(labels, label)
    print('Number of species: {}'.format(num_species))
    # images = np.array(images)
    images = np.reshape(images, (-1, img_width, img_height, 3))

    # Cast np array to keras default float type ('float32')
    images = K.cast_to_floatx(images)

    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels = to_categorical(labels,
                            num_classes=num_species)
    labels = K.cast_to_floatx(labels)

    print('Images shape: ', images.shape)
    print('Images dtype: ', images.dtype)
    print('Labels shape: ', labels.shape)
    print('Labels dtype: ', labels.dtype)

    return images, labels, num_species


# Training, validation and test split
###############################################################################


def train_val_test_split(images,
                         labels,
                         test_size=0.1,
                         val_size=0.135):
    """Split the data in a training, validation and test set. You can specify
    the test size and validation size. The set will be split in to test -
    training+validation first, and then training - validation will be split.

    Args:
        images (array): all images as 4d array.
        labels (array): all labels in relation to the images.
        test_size (float): size of the training set. default is 10%.
        val_size (float): size of the validation set, `0.135` is around 15
            percent of the total input set..

    Returns:
        arrays: Returns the split arrays of images and labels for training,
            validation and testing.

    """
    sss = StratifiedShuffleSplit(n_splits=1,
                                 test_size=test_size,
                                 random_state=seed)
    sss.get_n_splits(images,
                     labels)

    for train_index, test_index in sss.split(images,
                                             labels):
        # print('TEST (10%%): {}'.format(test_index))
        X_train, X_test = images[train_index], images[test_index]
        Y_train, Y_test = labels[train_index], labels[test_index]

        sss = StratifiedShuffleSplit(n_splits=1,
                                     test_size=val_size,
                                     random_state=seed)
        sss.get_n_splits(X_train,
                         Y_train)

        for train_index, val_index in sss.split(X_train,
                                                Y_train):
            # print('\nTRAIN (~75%%): {} \n\nVAL (~15%%): {}'.format(
            #     train_index, val_index))
            X_train, X_val = X_train[train_index], X_train[val_index]
            Y_train, Y_val = Y_train[train_index], Y_train[val_index]

        nb_specimens = len(X_test) + len(X_train) + len(X_val)
        print('Number of X_test: {}'.format(len(X_test)))
        print('Number of X_train: {}'.format(len(X_train)))
        print('Number of X_val: {}'.format(len(X_val)))
        print('Total number of images: {}'.format(nb_specimens))

        return X_train, Y_train, X_val, Y_val, X_test, Y_test


def load_data(datadir, config, shottype='h'):
    """Combining the loading of images and labels together with the splitting
    function.

    Args:
        datadir (path): The data directory that contains the `images` folder.
        shottype (str): Specifie the shottype using the following options:
            - `h` (head),
            - `d` (dorsal)
            - `p` (profile).
            Defaults to `h`.

    Returns:
        arrays: Arrays of images and labels for training, validation and
            testing.

    """
    img_width, img_height = image_size(config=config)

    images, labels, num_species = img_load_shottype(
        shottype=shottype,
        datadir=datadir,
        img_height=img_height,
        img_width=img_width)

    X_train, Y_train, X_val, Y_val, X_test, Y_test = train_val_test_split(
        images=images,
        labels=labels,
        test_size=0.1,
        val_size=0.135)

    return X_train, Y_train, X_val, Y_val, X_test, Y_test, num_species

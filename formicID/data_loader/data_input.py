################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  data_input                                  #
################################################################################
'''Description:
`data_input.py` can import data from files in folders. If data is downloaded
using the scraper script the files should be in a correct folder structure
(divided per shottype and species). The script also encodes labels and
preprocesses the images into the right format (RGB and [-1, 1] range). With
`train_val_test_split` the data can be split in 3 subsets: Training, validation
and test sets. You can set the splits.

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
################################################################################

import os

import numpy as np
from keras import backend as K
from keras.utils import normalize, to_categorical
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder

import cv2
from tqdm import tqdm
from utils.utils import wd

# Parameters and settings
################################################################################
seed = 1337
img_width, img_height = 140, 140

# Load images
################################################################################


def img_load_shottype(shottype, datadir):
    """This function loads images from a directory for which the shottype is
    given.

    Args:
        shottype (str): Specifies the shottype:
            - `h` (head),
            - `d` (dorsal)
            - `p` (profile)
        datadir (str): The data directory that contains the `images` folder.

    Returns:
        images (array): images as numpy 4D arrays (batches, width, height,
        channels).
        labels (array): labels as numpy 2d arrays (batches, labels).
    """
    # TODO (MJABOER):
    # Normalize image data (see datagenerators)

    data_dir = os.path.join(wd, 'data', datadir, 'images')
    if shottype == 'h':
        data_dir = os.path.join(data_dir, 'head')
    if shottype == 'd':
        data_dir = os.path.join(data_dir, 'dorsal')
    if shottype == 'p':
        data_dir = os.path.join(data_dir, 'profile')

    images = []
    labels = []
    print('Reading images from "{}"'.format(data_dir))
    for species in tqdm(os.listdir(data_dir),
                        desc='Reading folders',
                        unit='species'):
        num_species = len(species)
        print('Number of species: {}'.format(num_species))
        for image in tqdm(os.listdir(os.path.join(data_dir, species)),
                          desc='Loading {}'.format(species),
                          unit='images'):
            if '.jpg' in image:
                img = cv2.imread(os.path.join(data_dir, species, image))
                img = cv2.resize(img,
                                 (img_width, img_height),
                                 interpolation=cv2.INTER_AREA)
                img = np.asarray(img)
                # returns BGR instead of RGB
                if img is not None:
                    img = img[:, :, ::-1]  # Convert to RGB (inception_v3)
                    images = np.append(images, img)
            label = species
            labels = np.append(labels, label)
    print('\n')  # to correctly print tqdm when finished.
    images = np.reshape(images, (-1, img_width, img_height, 3))
    images /= 255. # normalization step
    images -= 0.5
    images *= 2
    # Cast np array to keras default float type ('float32')
    images = K.cast_to_floatx(images)
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    # divide by 2, because of the recursive call to data_dir
    labels = to_categorical(labels, num_classes=num_species)
    labels = K.cast_to_floatx(labels)

    # print('after', labels)
    # print('\nImages shape: ',images.shape)
    # print('images dtype: ', images.dtype)
    # print('labels shape: ', labels.shape)
    # print('labels dtype: ', labels.dtype)

    return images, labels


# Training, validation and test split
################################################################################


def train_val_test_split(images, labels, test_size=0.1, val_size=0.135):
    """Using this function you can split the data in a training, validation and test set. You can specify the test size and validation size. The set will be split in to test - training+validation first, and then training - validation will be split.

    Args:
        images (type): all images as 4d array.
        labels (type): all labels in relation to the images.
        test_size (type): size of the training set. default is 10%.
        val_size (type): size of the validation set, `0.135` is around 15
            percent of the total input set..

    Returns:
        type: Description of returned object.
    """
    sss = StratifiedShuffleSplit(
        n_splits=1, test_size=test_size, random_state=seed)
    sss.get_n_splits(images, labels)
    # print(sss)
    for train_index, test_index in sss.split(images, labels):
        # print('TEST (10%%): {}'.format(test_index))
        X_train, X_test = images[train_index], images[test_index]
        Y_train, Y_test = labels[train_index], labels[test_index]

        sss = StratifiedShuffleSplit(
            n_splits=1, test_size=val_size, random_state=seed)
        sss.get_n_splits(X_train, Y_train)
        # print(sss)
        for train_index, val_index in sss.split(X_train, Y_train):
            # print('\nTRAIN (~75%%): {} \n\nVAL (~15%%): {}'.format(
            #     train_index, val_index))
            X_train, X_val = X_train[train_index], X_train[val_index]
            Y_train, Y_val = Y_train[train_index], Y_train[val_index]

        nb_specimens = len(X_test) + len(X_train) + len(X_val)
        print('Number of X_test: {}'.format(len(X_test)))
        print('Number of X_train: {}'.format(len(X_train)))
        print('Number of X_val: {}'.format(len(X_val)))
        print('Number of labels: {}'.format(nb_specimens))

        return X_train, Y_train, X_val, Y_val, X_test, Y_test

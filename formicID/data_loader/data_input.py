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

# Standard library imports
import logging
import os
import random
import shutil

# Deeplearning tools imports
from keras import backend as K
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.utils import normalize
from keras.utils import to_categorical

# Data tools imports
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder

# Additional project imports
from tqdm import tqdm

# FormicID imports
from utils.utils import wd

# Parameters and settings
###############################################################################


# Create image loading csvfile
###############################################################################


def make_image_path_csv(dataset):
    dataset = os.path.join('data', dataset)
    image_dir = os.path.join(dataset, 'images')
    path_col = []
    shottype_col = []
    species_col = []
    identifier_col = []
    for shottype in os.listdir(image_dir):
        for species in os.listdir(os.path.join(image_dir, shottype)):
            for image in os.listdir(os.path.join(image_dir,
                                                 shottype,
                                                 species)):
                if image.endswith('.jpg'):
                    identifier = os.path.split(image)[1].split('_')[2]
                    image = os.path.join(image_dir, shottype, species, image)
                    path_col.append(image)
                    shottype_col.append(shottype)
                    species_col.append(species)
                    identifier_col.append(identifier)
    data = list(zip(identifier_col, species_col, shottype_col, path_col))
    df = pd.DataFrame(data,
                      columns=['identifier',
                               'species',
                               'shottype',
                               'path'])
    output_csv = os.path.join(dataset, 'image_path.csv')
    df.to_csv(path_or_buf=output_csv,
              header=True,
              index=False,
              sep=",")

# Split training/validation/test in folder
###############################################################################


def split_in_directory(dataset,
                       shottype='head',
                       test_split=0.1,
                       val_split=0.2):
    """Split the image files for all species into subfolders for a training,
    validation and test set.

    Args:
        dataset (str): Directory that holds the shottype folders with species
            and images.
        shottype (str): The shottype folder. Defaults to 'head'.
        test_split (float): Percentage of images for the test set. Defaults to
            0.1.
        val_split (float): Percentage of images for the validation set.
            Defaults to 0.2.

    """
    val_split = val_split + test_split
    input_dir = os.path.join(wd, 'data', dataset, 'images', shottype)
    dirs_split = ['1-training', '2-validation', '3-test']
    for dir in dirs_split:
        if os.path.exists(os.path.join(input_dir, dir)):
            # TODO: Fix a better statement for stopping...
            logging.info('Files are already split in training, validation and '
                         'testing sets. Files will not be split again.')
            return
        else:
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
    for species in tqdm(os.listdir(input_dir),
                        description='Splitting into subsets'):
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

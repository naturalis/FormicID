###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  data_input                                 #
###############################################################################
"""Description:
These scripts are utilities for the data input. It is possible to split the
data into training, validation and test sets in two ways. First by randomly
copying images into training, validation and test directories or second by
creating a training, validation and test csv file, containing paths to the
original images. It is also possible to remove reproductive specimens, using a
list of catalog numbers of reproductives, from a test set.

Initially, images should be in the following folder structure, see below. This
should be the case if you downloaded the images using the scripts in this
project.
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

"""

# Packages
###############################################################################

# Standard library imports
import logging
import os
import random
import shutil

# Data tools imports
import pandas as pd
from sklearn.model_selection import train_test_split

# Additional project imports
from tqdm import tqdm

# Create image loading csvfiles
###############################################################################


def image_path_csv(config):
    """Split the image path csv file in a training, validation and test image
    path csv file, using the validation and test split numbers defined in the
    configuration file.

    Args:
        config (Bunch object): The JSON configuration Bunch object.

    """
    test_split = config.test_split
    val_split = config.val_split
    seed = config.seed
    dataset = os.path.join("data", config.data_set)
    image_dir = os.path.join(dataset, "images")
    path_col = []
    shottype_col = []
    species_col = []
    identifier_col = []
    for shottype in os.listdir(image_dir):
        for species in os.listdir(os.path.join(image_dir, shottype)):
            for image in os.listdir(
                os.path.join(image_dir, shottype, species)
            ):
                if image.endswith(".jpg"):
                    identifier = os.path.split(image)[1].split("_")[2]
                    image = os.path.join(image_dir, shottype, species, image)
                    path_col.append(image)
                    shottype_col.append(shottype)
                    species_col.append(species)
                    identifier_col.append(identifier)
    data = list(zip(identifier_col, species_col, shottype_col, path_col))
    df = pd.DataFrame(
        data, columns=["identifier", "species", "shottype", "path"]
    )
    x = df
    y = df.species
    train, test = train_test_split(
        df, test_size=test_split, shuffle=True, random_state=seed, stratify=y
    )
    y2 = train.species
#     Fix the train and val to csv naming
    val, train = train_test_split(
        train,
        test_size=val_split,
        shuffle=True,
        random_state=seed,
        stratify=y2,
    )
    train.to_csv(
        path_or_buf=os.path.join(dataset, "image_path_val.csv"),
        header=True,
        index=False,
        sep=",",
    )
    val.to_csv(
        path_or_buf=os.path.join(dataset, "image_path_train.csv"),
        header=True,
        index=False,
        sep=",",
    )
    test.to_csv(
        path_or_buf=os.path.join(dataset, "image_path_test.csv"),
        header=True,
        index=False,
        sep=",",
    )


# Split training/validation/test images to their own folder
###############################################################################


def split_in_directory(config, bad=None):
    """Copies and split the image files for all species folders into
    subfolders for a training, validation and test set, called respectively
    `1-training`, `2-validation` and `3-test`.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        bad (str): Point to a csv file containing catalog numbers of bad
            specimens, if you wish to ommit these from the training,
            validation and test set. Defaults to None.

    """
    dataset = config.data_set
    shottype = config.shottype
    test_split = config.test_split
    val_split = config.val_split + config.test_split
    input_dir = os.path.join("data", dataset, "images", shottype)
    dirs_split = ["1-training", "2-validation", "3-test"]
    for dir in dirs_split:
        if os.path.exists(os.path.join(input_dir, dir)):
            # TODO: Fix a better statement for stopping...
            logging.info(
                "Files are already split in training, validation and "
                "testing sets. Files will not be split again."
            )
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
    if bad is not None:
        bad_data = pd.read_csv(bad, header=0)
        bad_list = list(bad_data.Catalog_number)
        bad_list = [x.lower() for x in bad_list]
        print(
            "Ommitting {} specimens for {} shottype.".format(
                len(bad_list),
                shottype
                # TODO: is the length of bad_list also counting header?
            )
        )
    for species in tqdm(os.listdir(input_dir), desc="Splitting into subsets"):
        if species in dirs_split:
            continue

        nb_images = len(os.listdir(os.path.join(input_dir, species)))
        image_files = os.listdir(os.path.join(input_dir, species))
        shuffled = image_files[:]
        random.shuffle(shuffled)
        num1 = round(len(shuffled) * test_split)
        num2 = round(len(shuffled) * val_split)
        to_test, to_val, to_train = (
            shuffled[:num1],
            shuffled[num1:num2],
            shuffled[num2:],
        )
        for image in os.listdir(os.path.join(input_dir, species)):
            if image.endswith(".jpg"):
                for img in to_test:
                    if bad_list is not None:
                        if (
                            any(catal in img.split("_") for catal in bad_list)
                            is False
                        ):
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(test_dir, species, img),
                            )
                        else:
                            continue

                for img in to_val:
                    if bad_list is not None:
                        if (
                            any(catal in img.split("_") for catal in bad_list)
                            is False
                        ):
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(val_dir, species, img),
                            )
                        else:
                            continue

                for img in to_train:
                    if bad_list is not None:
                        if (
                            any(catal in img.split("_") for catal in bad_list)
                            is False
                        ):
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(train_dir, species, img),
                            )
                        else:
                            continue


# remove reproductives from test sets
###############################################################################


def remove_reproductives(csv, dataset, config):
    """Remove reproductives by supplying the catalognumber..

    Args:
        csv (str): csv file that holds the catalog numbers.
        dataset (str): Name of the dataset, that holds the test set, of which
            the reproductives should be removed.
        config (Bunch object): The JSON configuration Bunch object.

    """
    shottype = config.shottype
    input_dir = os.path.join("data", dataset, "images", shottype, "3-test")
    reproductives = pd.read_csv(csv, header=0)
    repro_list = list(reproductives.Catalog_number)
    repro_list = [x.lower() for x in repro_list]
    i = 0
    for species in tqdm(os.listdir(input_dir), desc="Removing reproductives"):
        for image in tqdm(
            os.listdir(os.path.join(input_dir, species)),
            desc="Checking species folders.",
        ):
            if image.endswith(".jpg"):
                if (
                    any(catal in image.split("_") for catal in repro_list)
                    is True
                ):
                    os.remove(os.path.join(input_dir, species, image))
                    i += 1
    print("{} reproductive specimens were removed.".format(i))

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
These scripts will sort out the images so they can be loaded by a trainer
function. One function could split folders containing images in different
subsets. The other function can create training, validation, test csv files
with the pathway to the images stored in them. If data is downloaded using the
scraper script the files should be in a correct folder structure (divided per
shottype and species). The files should be structured as follows:

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
        print("Ommitting {} specimens for {} shottype.".format(len(bad_list), shottype))
    for species in tqdm(os.listdir(input_dir), desc="Splitting into subsets"):
        if species in dirs_split:
            continue

        nb_images = len(os.listdir(os.path.join(input_dir, species)))
        image_files = os.listdir(os.path.join(input_dir, species))
        shuffled = image_files[:]
        random.shuffle(shuffled)
        num1 = round(len(shuffled) * test_split)
        num2 = round(len(shuffled) * val_split)
        # fmt: off
        to_test, to_val, to_train = shuffled[:num1], shuffled[
            num1:num2], shuffled[num2:]
        # fmt: on
        for image in os.listdir(os.path.join(input_dir, species)):
            if image.endswith(".jpg"):
                for img in to_test:
                    if bad_list is not None:
                        if any(catal in img.split("_") for catal in bad_list) is False:
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(test_dir, species, img),
                            )
                        else:
                            print("{} is ommitted for copying to a training, validation or testing folder.".format(img))
                            continue

                for img in to_val:
                    if bad_list is not None:
                        if any(catal in img.split("_") for catal in bad_list) is False:
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(val_dir, species, img),
                                )
                        else:
                            print("{} is ommitted for copying to a training, validation or testing folder.".format(img))
                            continue

                for img in to_train:
                    if bad_list is not None:
                        if any(catal in img.split("_") for catal in bad_list) is False:
                            shutil.copy2(
                                os.path.join(input_dir, species, img),
                                os.path.join(train_dir, species, img),
                            )
                        else:
                            print("{} is ommitted for copying to a training, validation or testing folder.".format(img))
                            continue

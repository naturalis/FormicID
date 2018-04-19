###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                     Scraper                                 #
#                                                                             #
###############################################################################
"""Description:
Use this script to updating the csv file for broken URLs. After that you can
download all images. The images will be saved in different folders per shot
type and per species.
"""

# Packages
###############################################################################

# Standard library imports
import itertools
import logging
import os
import re
from urllib.error import HTTPError
from urllib.request import urlretrieve

# Data tools imports
import csv
import pandas as pd

# Additional project imports
import requests
from tqdm import tqdm

# FormicID imports
from AntWeb.AW2_to_json import urls_to_json
from AntWeb.json_to_csv import batch_json_to_csv
from data_loader.data_input import image_path_csv

# Parameters and settings
###############################################################################


# Make changes to the csv file
###############################################################################


def _csv_update(dataset, csvfile):
    """This function will remove broken links to a different csvfile.

    Args:
        dataset (str): The dataset (directory), that holds the csv with image
            URLs and names.
        csvfile (str): A csv file that contains all the specimen and image
            information with 4 columns, namely:
                - 'catalog_number',
                - 'scientific_name',
                - 'shot_type',
                - 'image_url'

    Returns:
        csv file: A cleaned csv file ready for downloading images.

    Raises:
        AssertionError: When the `csvfile` is not a csv file.

    """
    if not csvfile.endswith(".csv"):
        raise AssertionError(
            "This is not a csv file: {}. Please use a csv ",
            "file and specify the suffix".format(csvfile),
        )

    columns = ["catalog_number", "scientific_name", "shot_type", "image_url"]
    with open(csvfile, "rt") as csv_open:
        df = pd.read_csv(csv_open, sep=",")
        specimens = pd.DataFrame(df, columns=columns)
        specimen_blf = df[df["image_url"].str.contains("blf") == True]
        specimen_hjr = df[df["image_url"].str.contains("hjr") == True]
        frames = [specimen_blf, specimen_hjr]
        specimen_bad = pd.concat(objs=frames)
        df2 = pd.DataFrame(columns=columns)
        for index, row in tqdm(
            specimen_bad.iterrows(), desc="Fixing image URLs", unit="URLs"
        ):
            row.image_url = re.sub("_", "(", row.image_url, count=1)
            row.image_url = re.sub("_", ")", row.image_url, count=1)
            row.image_url = re.sub("_", "(", row.image_url, count=1)
            row.image_url = re.sub("_", ")", row.image_url, count=1)
            df2 = df2.append(row)
        specimen_bad.update(df2)
        df3 = pd.DataFrame(columns=columns)
        for index, row in tqdm(
            specimen_bad.iterrows(), desc="Fixing catalog numbers", unit="URLs"
        ):
            row.catalog_number = re.sub("_", "(", row.catalog_number, count=1)
            row.catalog_number = re.sub("_", ")", row.catalog_number, count=1)
            df3 = df3.append(row)
        specimen_bad.update(df3)
        df.update(specimen_bad)
        df.to_csv(csvfile, sep=",", columns=columns, index=False)


# Downloading of images
###############################################################################


def image_scraper(
    csvfile, dataset, shottypes="hdp", start=None, end=None, update=False
):
    """This function scrapes images of urls found in the csv file that is made
    with the download_to_csv function. It will check if files already exist.
    If a file already exists, it will not be downloaded again.

    Args:
        csvfile (str): Name of the csvfile in the `data` folder.
        dataset (str): Name of the dataset (directory).
        shottypes (str): One, two or all of `h`, `d`, `p`. Defaults to `hdp`.
        start (int): Set the starting row for downloading. Defaults to `None`.
        end (int): Set the end row for downloading. Defaults to `None`.
        update (bool): If [default=True]; the csv_update() function will be
            called. Defaults to `False`.

    """
    csvfile = os.path.join("data", dataset, csvfile)
    if update == True:
        logging.info(
            "Update argument has been set to: True. Updating file " "now..."
        )
        _csv_update(dataset=dataset, csvfile=csvfile)
        logging.info("The csv file has been updated.")
    else:
        logging.info("Update argument has been set to: False.")
    logging.info("Checking Folders...")
    if not os.path.exists(os.path.join("data", dataset, "images")):
        os.mkdir(os.path.join("data", dataset, "images"))
        if "h" in shottypes:
            os.mkdir(os.path.join("data", dataset, "images", "head"))
        if "d" in shottypes:
            os.mkdir(os.path.join("data", dataset, "images", "dorsal"))
        if "p" in shottypes:
            os.mkdir(os.path.join("data", dataset, "images", "profile"))
        logging.info("Folders are created")
    if os.path.exists(os.path.join("data", dataset, "images", "head")):
        dir_h = os.path.join("data", dataset, "images", "head")
    if os.path.exists(os.path.join("data", dataset, "images", "profile")):
        dir_p = os.path.join("data", dataset, "images", "profile")
    if os.path.exists(os.path.join("data", dataset, "images", "dorsal")):
        dir_d = os.path.join("data", dataset, "images", "dorsal")
    nb_rows = sum(1 for line in open(csvfile))
    logging.info("The csv file contains {} images.".format(nb_rows))
    if end == None:
        end = nb_rows
    if start == None:
        start = 0
    nb_images = end - start
    with open(csvfile, "rt") as images:
        imagereader = csv.reader(itertools.islice(images, start, end + 1))
        logging.info("Starting to scrape {} images...".format(nb_images))
        for image in tqdm(
            imagereader,
            desc="Scraping images",
            total=nb_images,
            unit=" images",
        ):
            if image[3] != "image_url":  # Don't scrape the header line
                # Create a folder for the species in a shot type folder if it
                # does not exist already, then download the image.
                if "h" in shottypes.lower():
                    if image[2] == "h":
                        if not os.path.exists(os.path.join(dir_h, image[1])):
                            os.mkdir(os.path.join(dir_h, image[1]))
                        filename = os.path.join(
                            dir_h,
                            image[1],
                            "{}_{}_{}.jpg".format(
                                image[1], image[0], image[2]
                            ),
                        )
                        try:
                            if not os.path.isfile(filename):
                                urlretrieve(url=image[3], filename=filename)
                            else:
                                continue

                        except HTTPError as err:
                            if err.code == 404:
                                logging.error("Error 404: {}".format(image[3]))
                                continue

                if "d" in shottypes.lower():
                    if image[2] == "d":
                        if not os.path.exists(os.path.join(dir_d, image[1])):
                            os.mkdir(os.path.join(dir_d, image[1]))
                        filename = os.path.join(
                            dir_d,
                            image[1],
                            "{}_{}_{}.jpg".format(
                                image[1], image[0], image[2]
                            ),
                        )
                        try:
                            if not os.path.isfile(filename):
                                urlretrieve(url=image[3], filename=filename)
                            else:
                                continue

                        except HTTPError as err:
                            if err.code == 404:
                                logging.error("Error 404: {}".format(image[3]))
                                continue

                if "p" in shottypes.lower():
                    if image[2] == "p":
                        if not os.path.exists(os.path.join(dir_p, image[1])):
                            os.mkdir(os.path.join(dir_p, image[1]))
                        filename = os.path.join(
                            dir_p,
                            image[1],
                            "{}_{}_{}.jpg".format(
                                image[1], image[0], image[2]
                            ),
                        )
                        try:
                            if not os.path.isfile(filename):
                                urlretrieve(url=image[3], filename=filename)
                            else:
                                continue

                        except HTTPError as err:
                            if err.code == 404:
                                logging.error("Error 404: {}".format(image[3]))
                                continue

    logging.info("{} images were downloaded.".format(nb_images))


def get_dataset(
    input,
    n_jsonfiles,
    config,
    shottypes="hdp",
    quality="low",
    update=False,
    offset_set=0,
    limit_set=9999,
):
    """This function combines all the functions for finalizing the dataset.

    Args:
        input (file): The `genus` and `species` csv file.
        n_jsonfiles (int): Number of JSON files to be downloaded.
        config (Bunch object): The JSON configuration Bunch object.
        quality (str): Set the image quality when downloading the images. Each
            different image quality has its own unique link, that is why it
            needs to be set when filtering the JSON file. Set the quility to
            either one of (from highest quality to lowest): `high`,
            `thumbview`, `medium`, `low`. Defaults to `low`.
        update (Bool): If [default=True]; the csv_update() function will be
            called. Defaults to `False`.
        offset_set (int): The offset for downloading AntWeb records in
            batches. Defaults to `0`.
        limit_set (int): The limit for downloading a set of AntWeb records.
            Defaults to `9999`.

    """
    logging.info("Dataset creation is starting.")
    dataset_name = config.data_set
    urls_to_json(
        csv_file=input,
        dataset_name=dataset_name,
        n_jsonfiles=n_jsonfiles,
        offset_set=offset_set,
        limit_set=limit_set,
    )
    batch_json_to_csv(
        dataset=dataset_name,
        output_dir=dataset_name,
        quality=quality,
        csvname="image_urls.csv",
    )
    image_scraper(
        csvfile="image_urls.csv",
        dataset=dataset_name,
        shottypes=shottypes,
        # start=0,
        # end=1491,
        update=update,
    )
    image_path_csv(config=config)
    logging.info("The dataset is created.")

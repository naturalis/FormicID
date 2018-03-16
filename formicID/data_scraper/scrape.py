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
'''Description:
Use this script to updating the csv file for broken URLs. After that you can
download all images. The images will be saved in different folders per shot
type and per species.
'''

# Packages
###############################################################################
import csv
import itertools
import logging
import os
import re
from urllib.error import HTTPError
from urllib.request import urlretrieve

import pandas as pd
import requests
from tqdm import tqdm

from utils.utils import wd

# Parameters and settings
###############################################################################
data_dir = os.path.join(wd, 'data')


# Make changes to the csv file
###############################################################################


def csv_update(input_dir,
               csvfile):
    """This function will remove broken links to a different csvfile.

    Args:
        input_dir (str): the input directory containing the csvfile
        csvfile (str): A .csv file that contains all the specimen and image
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
    if not csvfile.endswith('.csv'):
        raise AssertionError('This is not a csv file: {}. Please use a csv ',
                             'file and specify the suffix'.format(csvfile))
    csvfile = os.path.join(data_dir,
                           input_dir,
                           csvfile)
    columns = ['catalog_number',
               'scientific_name',
               'shot_type',
               'image_url']
    with open(csvfile, 'rt') as csv_open:
        df = pd.read_csv(csv_open,
                         sep=',')
        specimens = pd.DataFrame(df,
                                 columns=columns)
        specimen_blf = df[df['image_url'].str.contains('blf') == True]
        specimen_hjr = df[df['image_url'].str.contains('hjr') == True]
        frames = [specimen_blf,
                  specimen_hjr]
        specimen_bad = pd.concat(objs=frames)
        df2 = pd.DataFrame(columns=columns)
        for index, row in tqdm(specimen_bad.iterrows(),
                               desc='Fixing image URLs',
                               unit='URLs'):
            row.image_url = re.sub('_', '(', row.image_url, count=1)
            row.image_url = re.sub('_', ')', row.image_url, count=1)
            row.image_url = re.sub('_', '(', row.image_url, count=1)
            row.image_url = re.sub('_', ')', row.image_url, count=1)
            df2 = df2.append(row)
        specimen_bad.update(df2)
        df3 = pd.DataFrame(columns=columns)
        for index, row in tqdm(specimen_bad.iterrows(),
                               desc='Fixing catalog numbers',
                               unit='URLs'):
            row.catalog_number = re.sub('_', '(', row.catalog_number, count=1)
            row.catalog_number = re.sub('_', ')', row.catalog_number, count=1)
            df3 = df3.append(row)
        specimen_bad.update(df3)
        df.update(specimen_bad)
        df.to_csv(csvfile, sep=',',
                  columns=columns,
                  index=False)


# Downloading of images
###############################################################################


def image_scraper(csvfile,
                  input_dir,
                  dir_out_name,
                  start=None,
                  end=None,
                  update=False):
    """This function scrapes images of urls found in the csv file that is made
    with the download_to_csv function.

    Args:
        csvfile (str): name of the csvfile in the `data` folder.
        input_dir (str): Name of the directory in `data` that contains the csv.
        dir_out_name (str): Name of the output folder, with the current
            date as prefix, which is created in the input_dir.
        start (int): Set the starting row for downloading. Defaults to `None`.
        end (int): Set the end row for downloading. Defaults to `None`.
        update (bool): if [default=True]; the csv_update() function will be
            called. Defaults to `False`.

    Returns:
        files: A folder with images.

    """
    csvfile = os.path.join(data_dir,
                           input_dir,
                           csvfile)
    if update == True:
        logging.info('Update argument has been set to: True. Updating file '
                     'now...')
        csv_update(input_dir=input_dir,
                   csvfile=csvfile)
        logging.info('The csv file has been updated.')
    else:
        logging.info('Update argument has been set to: False.')
    logging.info('Checking Folders...')
    if not os.path.exists(os.path.join(data_dir, input_dir, dir_out_name)):
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'head'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'dorsal'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'profile'))
        logging.info('Folders are created')
    dir_h = os.path.join(data_dir, input_dir, dir_out_name, 'head')
    dir_d = os.path.join(data_dir, input_dir, dir_out_name, 'dorsal')
    dir_p = os.path.join(data_dir, input_dir, dir_out_name, 'profile')
    nb_rows = sum(1 for line in open(csvfile))
    logging.info('The csv file contains {} images.'.format(nb_rows))
    if end == None:
        end = nb_rows
    if start == None:
        start = 0
    nb_images = end - start
    with open(csvfile, 'rt') as images:
        imagereader = csv.reader(
            itertools.islice(images,
                             start,
                             end + 1))
        logging.info('Starting to scrape {} images...'.format(nb_images))
        for image in tqdm(imagereader,
                          desc='Scraping images',
                          total=nb_images,
                          unit=' images'):
            if image[3] != 'image_url':  # Don't scrape the header line
                # Create a folder for the species in a shot type folder if it
                # does not exist already, then download the image.
                if image[2] == 'h':
                    if not os.path.exists(os.path.join(dir_h, image[1])):
                        os.mkdir(os.path.join(dir_h, image[1]))
                    filename = os.path.join(dir_h, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                                                  image[0],
                                                                  image[2]))
                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            logging.error('Error 404: {}'.format(image[3]))
                            continue
                if image[2] == 'd':
                    if not os.path.exists(os.path.join(dir_d, image[1])):
                        os.mkdir(os.path.join(dir_d, image[1]))
                    filename = os.path.join(dir_d, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                                                  image[0],
                                                                  image[2]))
                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            logging.error('Error 404: {}'.format(image[3]))
                            continue
                if image[2] == 'p':
                    if not os.path.exists(os.path.join(dir_p, image[1])):
                        os.mkdir(os.path.join(dir_p, image[1]))
                    filename = os.path.join(dir_p, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                                                  image[0],
                                                                  image[2]))
                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            logging.error('Error 404: {}'.format(image[3]))
                            continue
        logging.info('{} images were downloaded.'.format(nb_images))

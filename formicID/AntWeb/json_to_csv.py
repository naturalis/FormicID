###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  ANTWEB API                                 #
#                                  JSON 2 csv                                 #
###############################################################################
'''Description:
Iterate over a number of JSON files in a folder and save relevant information
in a csv file (containing a `catalog_number`, `scientific_name`, `shot_type`,
and `image_url`) ready for `scrape.py`.
'''
# Packages
###############################################################################

# Standard library imports
import logging
import os

# Data tools imports
import jmespath
import json
import pandas as pd

# Additional project imports
from tqdm import tqdm

# FormicID imports
from utils.utils import today_timestr

# Parameters and settings
###############################################################################


# Extract needed information
###############################################################################


def _filter_json(
    json_file,
    quality
):
    """Load a JSON object and filter for only relevant values using a set
    quality for images.

    Args:
        json_file (JSON object): A JSON object with AntWeb data, downloaded
            using the `urls_to_json()` function from `AW2_to_json.py`.
        quality (str): Set the image quality when downloading the images. Each
            different image quality has its own unique link, that is why it
            needs to be set when filtering the JSON file. Set the quility to
            either one of (from highest quality to lowest): `high`,
            `thumbview`, `medium`, `low`. Defaults to `low`.

    Returns:
        list: A list of
            [`catalog_number`,
            `scientific_name`,
            `shot_type`,
            `image_url`].

    Raises:
        AssertionError: When the quality is not set to a correct argument.

    """
    if quality not in ['high', 'low', 'medium', 'thumbview']:
        raise AssertionError('Quality should be set to one of `high`, `low`,'
                             '`medium`, `thumbview`. {} is a wrong argument '
                             'for quality.'.format(quality))
    if quality == 'high':
        qlty = 0
    if quality == 'low':
        qlty = 1
    if quality == 'medium':
        qlty = 2
    if quality == 'thumbview':
        qlty = 3
    json_txt = json.load(json_file)
    data_filtered = jmespath.search('specimens[].[catalogNumber,'
                                    'scientific_name, images."1".shot_types]',
                                    json_txt)
    lst = []
    for row in data_filtered:
        if row[2] != None:
            catalog_number = row[0]
            scientific_name = row[1]
            image_url = {}
            if 'h' in row[2]:
                image_url['h'] = row[2]['h']['img'][qlty]
            if 'p' in row[2]:
                image_url['p'] = row[2]['p']['img'][qlty]
            if 'd' in row[2]:
                image_url['d'] = row[2]['d']['img'][qlty]
            for key in image_url:
                new_row = [catalog_number,
                           scientific_name,
                           key,
                           image_url[key]]
                lst.append(new_row)
    return lst


# Filter batches of josn files to a csv file
###############################################################################


def batch_json_to_csv(
    csvname,
    dataset,
    quality='low',
    output_dir=None,
    overwrite=False
):
    """From a json file or batch of json files a csvfile is created with
    relevant information for downloading the images and naming the files.

    Args:
        csvname (str): Name of the output csv file.
        dataset (str): The name of the dataset (directory).
        quality (str): Set the image quality when downloading the images. Each
            different image quality has its own unique link, that is why it
            needs to be set when filtering the JSON file. Set the quility to
            either one of (from highest quality to lowest): `high`,
            `thumbview`, `medium`, `low`. Defaults to `low`.
        output_dir (str): name of the output directory. Defaults to `None`. If
            `None`, the images will be placed in an `image` subfolder in the
            dataset directory.
        overwrite (bool): Whether to overwrite the csv file with (new) json
            data, if the csv file already exists.

    Returns:
        file: A csv file containing the necesarry information for the scrape
            function.

    Raises:
        AssertionError: When there are no files in the input directory.

    """
    logging.info('Image quality for downloading is set to `{}`'.format(
        quality))
    input_direc = os.path.join('data',
                               dataset,
                               'json_files')
    if output_dir == None or output_dir == dataset:
        output_dir = os.path.join('data',
                                  dataset)
    else:
        outputdir = os.mkdir(os.path.join('data',
                                          output_dir))
    if not os.path.isfile(os.path.join(output_dir, csvname)):
        pass
    if os.path.isfile(os.path.join(output_dir, csvname)):
        if overwrite == False:
            logging.info('Csv file already exists, and will not be '
                         'overwritten, due to `overwrite` is set to `False`.')
        else:
            pass
    else:
        nb_files = len(os.listdir(input_direc))
        if nb_files == 0:
            raise AssertionError('There are no files in the input directory.')
        df2 = pd.DataFrame()
        columns = ['catalog_number',
                   'scientific_name',
                   'shot_type',
                   'image_url']
        for filename in tqdm(os.listdir(input_direc),
                             desc='Converting JSON files to csv',
                             total=nb_files,
                             unit='JSON files'):
            if filename.endswith('.json'):
                with open(os.path.join(input_direc,
                                       filename)) as data_file:
                    lst = _filter_json(data_file, quality=quality)
                    df = pd.DataFrame(lst,
                                      columns=columns)
                    df2 = df2.append(df)
        # replace spaces between genus and species names with underscores
        df2.replace('\s+', '_',
                    regex=True,
                    inplace=True)
        df2.columns = columns
        df2.to_csv(os.path.join(output_dir,
                                csvname),
                   index=False,
                   header=True)
    logging.info('All JSON files are read, filtered and added to the csv '
                 'file. "{0}" was created in {1}'.format(csvname,
                                                         output_dir))
    data_info = os.path.join('data', dataset,
                             'Info_' + dataset + '.txt')
    if not os.path.isfile(data_info):
        with open(data_info, 'wt') as txt:
            txt.write(
                'The dataset was downloaded on date: {0}'.format(
                    today_timestr))

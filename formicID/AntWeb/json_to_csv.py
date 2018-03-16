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

import json
import logging
import os

import jmespath
import pandas as pd
from tqdm import tqdm

from utils.utils import wd

# Parameters and settings
###############################################################################


# Extract needed information
###############################################################################


def filter_json(json_file):
    """Load a JSON object and filter for only relevant values.

    Args:
        json_file (JSON object): a JSON object with AntWeb data, downloaded
            using the `urls_to_json()` function from `AW2_to_json.py`.

    Returns:
        list: A list of
            [`catalog_number`,
            `scientific_name`,
            `shot_type`,
            `image_url`].

    """
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
                image_url['h'] = row[2]['h']['img'][1]
            if 'p' in row[2]:
                image_url['p'] = row[2]['p']['img'][1]
            if 'd' in row[2]:
                image_url['d'] = row[2]['d']['img'][1]
            for key in image_url:
                new_row = [catalog_number,
                           scientific_name,
                           key,
                           image_url[key]]
                lst.append(new_row)
    return lst


# Filter batches of josn files to a csv file
###############################################################################


def batch_json_to_csv(csvname,
                      input_dir,
                      output_dir=None):
    """From a json file or batch of json files a csvfile is created with
    relevant information for downloading the images and naming the files.

    Args:
        csvname (str): Name of the output csv file.
        input_dir (str): the name of the data directory holding the json files
            inside the `data` folder.
        output_dir (str): name of the output directory. Defaults to `None`. If
            `None`, the images will be placed in the the input_dir in an
            folder named `images`.

    Returns:
        file: A csv file containing the necesarry information for the scrape
            function.

    Raises:
        AssertionError: When there are no files in the input directory.

    """
    input_direc = os.path.join(wd,
                               'data',
                               input_dir,
                               'json_files')
    if output_dir == None or output_dir == input_dir:
        output_dir = os.path.join(wd,
                                  'data',
                                  input_dir)
    else:
        outputdir = os.mkdir(os.path.join(wd,
                                          'data',
                                          output_dir))
    nb_files = len(os.listdir(input_direc))
    if nb_files == 0:
        raise AssertionError('There are no files in the input directory.')
    df2 = pd.DataFrame()
    columns = ['catalog_number',
               'scientific_name',
               'shot_type',
               'image_url']
    for filename in tqdm(os.listdir(input_direc),
                         desc='Reading JSON files',
                         total=nb_files,
                         unit='JSON-files'):
        if filename.endswith('.json'):
            with open(os.path.join(input_direc,
                                   filename)) as data_file:
                lst = filter_json(data_file)
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
                 'file. "\n{0}" was created in {1}'.format(csvname,
                                                           output_dir))

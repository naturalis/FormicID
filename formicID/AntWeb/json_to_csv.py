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
import os

import jmespath
import pandas as pd

from tqdm import tqdm
from utils.utils import today_timestr, todaystr, wd

# Parameters and settings
###############################################################################


# Extract needed information
###############################################################################


def filter_json(json_file):
    """Load a JSON object and filter for only relevant values.

    Args:
        json_file (response object): a JSON object.

    Returns:
        type: A list of
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

            # print(row)
            catalog_number = row[0]
            scientific_name = row[1]
            image_url = {}

            # Take out urls for 'head', 'profile' and 'dorsal' shots
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


def batch_json_to_csv(input_dir,
                      output_dir,
                      csvname):
    """From a json or batch of json files a csvfile is created with relevant
    information for downloading the images and naming the files.

    Args:
        input_dir (str): Description of parameter `input_dir`.
        output_dir (str): path and name of the output directory.
        csvname (str): Description of parameter `csvname`.

    Returns:
        type: Creates a csv file in the output directory.

    """
    suffix = '.csv'
    input_direc = os.path.join(wd,
                               'data',
                               input_dir,
                               'json_files')

    output_dir = os.path.join(wd,
                              'data',
                              input_dir)

    nb_files = len(os.listdir(input_direc))

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
                            csvname + suffix),
               index=False,
               header=True)
    print('All JSON files are read, filtered and added to the csv file. \n'
          '{1}{2} was created in {3}'.format(csvname,
                                             suffix,
                                             output_dir))

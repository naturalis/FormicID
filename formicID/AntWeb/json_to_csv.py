################################################################################
#                                                                              #
#                                  xxx                                 #
#                                AntWeb to csv                                 #
################################################################################
'''
Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and will then create an csv file containing a
"catalog_number", "scientific_name", "shot_type", and "image_url"
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////

import requests
import json
import jmespath
import pandas as pd
import time
import datetime
import os
import csv
from functools import wraps
from urllib.request import urlretrieve
from tqdm import tqdm


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()


# Batch batch_filter_to_csv
# //////////////////////////////////////////////////////////////////////////////
def batch_filter_to_csv(directory):
    """
    # Description:
        Download all images found from a batch of JSON files in a directory

    # Input:
        directory = path and name of the output directory

    # Returns:
        creates a .csv file in the output directory

    # TODO:
        create input for:
        - the input directory
        - output directory
        - filename
    """
    df2 = pd.DataFrame()
    for filename in tqdm(os.listdir(directory),
                         desc='Reading JSON files'):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as data_file:
                # print('Filtering {}'.format(filename))
                lst = filter_json(data_file)
                df = create(lst)
                df2 = df2.append(df)

    # replace spaces between genus and species names with underscores
    df2.replace('\s+', '_', regex=True, inplace=True)
    df2.columns = [
        'catalog_number',
        'scientific_name',
        'shot_type',
        'image_url'
    ]
    # file_path = os.path.join(path, file_name)
    path = './data/top101-JSON/'
    file_name = 'top101.csv'
    df2.to_csv(os.path.join(path, file_name), index=False, header=True)
    print('All JSON files are read, filtered and added to the csv file.')

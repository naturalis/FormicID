###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                 ANTWEB API v2                               #
#                                AntWeb to json                               #
###############################################################################
'''Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and places the JSON file in a folder.
'''
# Packages
###############################################################################

import json
import logging
import os
import sys
import time
from csv import Sniffer

import pandas as pd
import requests
from tqdm import tqdm

from utils.utils import create_dirs, todaystr, wd

# Parameters and settings
###############################################################################


# Creating an URL
###############################################################################


def _create_url(limit,
               offset,
               **kwargs):
    """Creation of the url to access AntWebs API V2, using a base_url and
    arguments.

    Args:
        limit (int): sets the limit for accessing specimens.
        offset (int): sets the offset for accessing specimens.

    Args optional:
        genus (str): specifies the genus.
        species (str): specifies the species.
        country (str): specifies the country.
        caste (str): specifies the caste (does not work in API v2).

    Returns:
        URL object: Returns an URL as response object that can be opened by the
        function `request.get()`.

    """
    # Genus and species are optional arguments, not providing them will
    # download all species.
    genus = kwargs.get('genus', None)
    species = kwargs.get('species', None)
    country = kwargs.get('country', None)
    caste = kwargs.get('caste', None)
    base_url = 'http://www.antweb.org/api/v2/?'
    arguments = {    # API arguments for in the url
        'limit':        limit,
        'offset':       offset,
        'genus':        genus,
        'species':      species,
        'country':      country,
        'caste':        caste}  # not working
    url = requests.get(url=base_url,
                       params=arguments)
    return url


# Download JSON files from URLs
###############################################################################


def _get_json(input_url):
    """Scrapes JSON files from AntWeb URLs.

    Args:
        input_url (URL object): an URL containing a JSON object.

    Returns:
        JSON: A JSON object.

    Raises:
        AssertionError: If the json object contains nothing.

    """
    r = requests.get(url=input_url)
    data = r.json()
    if data != None:
        return data
    else:
        raise AssertionError('There is no JSON data in the url: {}.'.format(
            input_url.url))


def urls_to_json(csv_file,
                 input_dir,
                 output_dir,
                 offset_set=0,
                 limit_set=12000):
    """This function downloads JSON files for a list of species and places them
    in a drecitory. An limit_set higher than 12,000 will usually create
    problems. If you get 404 errors you will probably need to set the limit
    lower.

    Args:
        csv_file (str): the csv file genus and species names.
        input_dir (str): path to the directory that has the `csv_file`.
        output_dir (str): a new directory name, created in the `input_dir` for
            saving the JSON files.
        offset_set (int): the offset for downloading AntWeb records in
            batches. Defaults to `0`.
        limit_set (int): the limit for downloading a set of AntWeb records.
            Defaults to `9999`.

    Returns:
        A directory of JSON files for different species.

    Raises:
        ValueError: If `limit_set` is > 12,000.
        AssertionError: If `csv_file` is not a .csv file.
        AssertionError: If the csv file is not comma delimited.
        AssertionError: When the .csv does not have 2 columns.
        AssertionError: When the columns are not named correctly; `genus` and
            `species`.

    """
    if limit_set > 12000:
        raise ValueError('The `limit_set` should be lower than 12,000.')
    input_dir = os.path.join(wd, input_dir)
    output_dir = os.path.join(input_dir,
                              todaystr + '-' + output_dir,
                              'json_files')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if csv_file.endswith('.csv') == True:
        csv_file = os.path.join(input_dir,
                                csv_file)
    else:
        raise AssertionError('You have not set a `.csv` correctly.')
    logging.info('Reading {} and creating json_files folder.'.format(csv_file))
    with open(csv_file,
              'rt') as csv_open:
        dialect = Sniffer().sniff(csv_open.readline(), [',', ';'])
        csv_open.seek(0)
        if dialect.delimiter == ';':
            raise AssertionError('Please us a comma (,) delimited csv file ',
                                 'instead of {}.'.format(dialect.delimiter))
        csv_df = pd.read_csv(csv_open, sep=',')
        if len(csv_df.columns) != 2:
            raise AssertionError('The `.csv` should only have 2 column ',
                                 'instead of {} column(s).'.format(
                                     len(csv_df.columns)))
        if csv_df.columns.tolist() != ['genus', 'species']:
            raise AssertionError('The columns are not correctoly named: '
                                 '{} and {}. The column headers should be '
                                 'column 1: `genus` and column 2: '
                                 '`species`.'.format(
                                     csv_df.columns.tolist()))
        nb_indet = 0
        for index, row in csv_df.iterrows():
            if row['species'] == 'indet':
                nb_indet += 1
        logging.info('{} indet species found and will be skipped from '
                     'downloading.'.format(nb_indet))
        nb_specimens = csv_df.shape[0] - nb_indet
        for index, row in tqdm(csv_df.iterrows(),
                               total=nb_specimens,
                               desc='Downloading JSON files',
                               unit='Species'):
            url = create_url(limit=limit_set,
                             offset=offset_set,
                             genus=row['genus'],
                             species=row['species'])
            if row['species'] == 'indet':
                print('Skipping "{}".'.format(url.url))
            else:
                url = url.url
                logging.info('JSON downladed from URL: {}'.format(url))
                file_name = row['genus'] + '_' + row['species'] + '.json'
                species = get_json(url)
                with open(os.path.join(wd,
                                       output_dir,
                                       file_name), 'w') as jsonfile:
                    json.dump(species,
                              jsonfile)
                time.sleep(0.5)  # Sleep so AntWweb servers will not overload.
        logging.info('Downloading is finished. {} JSON files have been '
                     'downloaded'.format(nb_specimens))

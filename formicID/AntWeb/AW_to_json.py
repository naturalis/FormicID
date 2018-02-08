################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  ANTWEB API                                  #
#                                AntWeb to json                                #
################################################################################
'''
Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and places the JSON file in a folder.
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////

import datetime
import json
import os
import time

import pandas as pd
import requests

from tqdm import tqdm

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()
wd = os.getcwd()

# Creating an URL and get information
# //////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset, **kwargs):
    """Creation of the url to access AntWebs API, using a base_url and
    arguments.

    Args:
        limit (integer): sets the limit for accessing specimens.
        offset (integer): sets the offset for accessing specimens.
        **kwargs (type): Description of parameter `**kwargs`.
    Optional args:
        genus (type): specifies the genus
        species (type): specifies the species
        country (type): specifies the country
        caste (type): specifies the caste (does not work in API v2)

    Returns:
        type: Returns an URL as response object that can be opened by the
        function request.get()
    """
    # Genus and species are optional arguments
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
        'caste':        caste  # not working
    }
    # Creating the AntWeb url from the base url and the API arguments
    url = requests.get(url=base_url, params=arguments)

    return url


def get_url_info(input_url):
    """Provides status and information on the URL.

    Args:
        input_url (type): the url as response object, created by create_url().

    Returns:
        type: information on the URL

    """
    print('URL:', input_url.url)
    print('Connection status:', input_url.status_code)
    print('Time elapsed to connect to URL:', input_url.elapsed)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))

# Download JSON files from URLs
# //////////////////////////////////////////////////////////////////////////////
def get_json(input_url):
    """Scrapes JSON files from AntWeb URLs.

    Args:
        input_url (type): an URL containing a JSON object.

    Returns:
        type: A JSON object

    """

    r = requests.get(url=input_url)
    data = r.json()
    if data == None:
        print("JSON is empty!")
    else:
        return data


def urls_to_json(csv_file, output_dir, offset_set, limit_set):
    """This function downloads JSON files for a list of species and places them
    in a drecitory. An offset_set higher than 10,000 will usually create
    problems.

    Args:
        csv_file (type): path to the csv file genus and species names.
        output_dir (type): the directory for saving the JSON files.
        offset_set (type): set the offset for downloading AntWeb records in batches.
        limit_set (type): set a limit for downloading a set of records from AntWeb.

    Returns:
        A directory of JSON files for different species
    """
    csv_file = os.path.join(wd, csv_file)
    csvfile = pd.read_csv(csv_species, sep=';', header=0)
    nb_specimens = csvfile.shape[0]
    nb_batch = 1

    if not os.path.exists(os.join.path(wd, output_dir)):
        os.mkdir(os.join.path(wd, output_dir))

    for index, row in tqdm(csvfile.iterrows(), desc='Downloading JSON files'):
        url = create_url(
            limit=limit_set,
            offset=offset_set,
            genus=row['genus'],
            species=row['species'])
        url = url.url
        file_name = row['genus'] + '_' + row['species'] + '.json'
        species = get_json(url)
        with open(os.path.join(wd, output_dir, file_name), 'w') as jsonfile:
            json.dump(species, jsonfile)
        print('Creating URL, fechting JSON and writing to file ({} / '
              '{}).'.format(nb_batch, nb_specimens))
        nb_batch += 1
        time.sleep(0.5)


def main():
    urls_to_json(csv_species='./data/2018-01-09-db-Top101imagedspecies.csv',
                 output_dir='data/top101-JSON/'
                 offset_set=0,
                 limit_set=10000)


if __name__ == '__main__':
    main()

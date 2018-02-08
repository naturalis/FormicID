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
file for this genus+species and will then create an csv file containing a
"catalog_number", "scientific_name", "shot_type", and "image_url"
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////

import requests
import json
import pandas as pd
import time
import datetime
import os
from tqdm import tqdm


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()
wd = os.getcwd()

# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset, **kwargs):
    """
    # Description:
        Creation of the url to access AntWebs API, using a base_url and
        arguments

    # Input:
        - limit = sets the limit for accessing specimens
        - offset = sets the offset for accessing specimens
    # Optional input:
        - genus = specifies the genus
        - species = specifies the species
        - country = specifies the country
        - caste  = specifies the caste (e.g. worker) # does not work in API v2

    # Returns:
        Returns an URL as response object that can be opened by the function
        request.get()
    """
    # Make genus and species optional arguments for this function
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
    """
    # Description:
        Provides information on the URL

    # Input:
        - input_url = the url as response object, created by create_url()

    # Returns:
        returns information on the URL
    """
    # Get basic url information
    print('URL:', input_url.url)
    print('Connection status:', input_url.status_code)
    print('Time elapsed to connect to URL:', input_url.elapsed)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))


# get JSON > database
# //////////////////////////////////////////////////////////////////////////////


def get_json(input_url):
    """
    # Description:
        Scrapes JSON files from AntWeb URLs

    # Input:
        - input_url = an URL containing a JSON object

    # Returns:
        A JSON object
    """
    r = requests.get(url=input_url)
    data = r.json()
    if data == None:
        print("JSON is empty!")
    else:
        return data

# Executing
# //////////////////////////////////////////////////////////////////////////////


def urls_to_json(csv_file, output_dir, offset_set, limit_set):
    """
    # Description:
        This function downloads JSON files for a list of species and places them in a drecitory.

        limit / offset = number of batches to download
        630976 / 9859 = 64

    # Input:
        - csv_species = path to the csv file genus and species names
        - output_dir = the directory for saving the JSON files
        - offset_set = set the offset for downloading AntWeb records in batches
        - limit_set = set a limit for downloading a set of records from AntWeb

    # Returns:
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


# Executing
# //////////////////////////////////////////////////////////////////////////////
def main():
    urls_to_json(csv_species='./data/2018-01-09-db-Top101imagedspecies.csv',
                 output_dir='data/top101-JSON/'
                 offset_set=0,
                 limit_set=10000)


# //////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()

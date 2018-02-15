################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                 ANTWEB API v2                                #
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
################################################################################
todaystr = datetime.date.today().isoformat()
wd = os.getcwd()

# Creating an URL
################################################################################


def create_url(limit, offset, **kwargs):
    """Creation of the url to access AntWebs API V2, using a base_url and
    arguments.

    Args:
        limit (integer): sets the limit for accessing specimens.
        offset (integer): sets the offset for accessing specimens.
    Optional args (**kwargs):
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

    url = requests.get(url=base_url, params=arguments)

    return url

# Download JSON files from URLs
################################################################################


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


def urls_to_json(csv_file, input_dir, output_dir, offset_set, limit_set):
    """This function downloads JSON files for a list of species and places them
    in a drecitory. An limit_set higher than 10,000 will usually create
    problems.

    Args:
        csv_file (type): path to the csv file genus and species names.
        input_dir (type): path to the directory that has the csv file
        output_dir (type): a new directory name, created in the input_dir for
            saving the JSON files.
        offset_set (type): the offset for downloading AntWeb records in
            batches.
        limit_set (type): the limit for downloading a set of AntWeb records

    Returns:
        A directory of JSON files for different species
    """
    input_dir = os.path.join(wd, input_dir)
    output_dir = os.path.join(input_dir, todaystr + '-' +  output_dir, 'json_files')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(input_dir, csv_file)
    print('Reading {} and creating json_files folder...'.format(csv_file))
    with open(csv_file, 'rt') as csv_open:
        csv_df = pd.read_csv(csv_open, sep=';', header=0)

        nb_indet = 0
        for index, row in csv_df.iterrows():
            if row['species'] == 'indet':
                nb_indet += 1
        print('{} indet species '.format(nb_indet),
        'found and will be skipped from downloading.')

        nb_specimens = csv_df.shape[0] # - nb_indet

        if limit_set > 10000:
            raise ValueError('The limit_set should be lower than 10,000.')
        for index, row in tqdm(csv_df.iterrows(),
                               total=nb_specimens,
                               desc='Downloading JSON files',
                               unit='Species'):
            url = create_url(limit=limit_set, offset=offset_set,
                             genus=row['genus'], species=row['species'])
            if row['species'] == 'indet':
                print('Skipping "{}".'.format(url.url))
            else:
                url = url.url
                print('\nJSON downladed from URL:', url)
                file_name = row['genus'] + '_' + row['species'] + '.json'
                species = get_json(url)
                with open(os.path.join(wd, output_dir, file_name), 'w') as jsonfile:
                    json.dump(species, jsonfile)

                time.sleep(0.5) # wait 0.5s so AW does not crash
        print('Downloading is finished. {} JSON files '.format(nb_specimens),
        'have been downloaded')

# Main()
################################################################################

def main():
    urls_to_json(csv_file='2018-01-09-db-Top101imagedspecies.csv',
                 input_dir='data',
                 output_dir='test',
                 offset_set=0,
                 limit_set=9999)


if __name__ == '__main__':
    main()

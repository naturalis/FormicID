################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                 ANTWEB API v3                                #
#                                AntWeb to json                                #
################################################################################
'''
Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and places the JSON file in a folder.
'''
# Packages
################################################################################
import datetime
import json
import os
import time

import pandas as pd
import requests

from tqdm import tqdm
from utils.utils import todaystr, wd

# Parameters and settings
################################################################################

# Creating an URL
################################################################################
wd = os.getcwd()


def create_url(limit, offset, **kwargs):
    """Creation of the url to access AntWebs API V3, using a base_url and
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

    base_url = 'http://api.antweb.org/v3/taxaImages?'

    arguments = {    # API arguments for in the url
        'limit':        limit,
        'offset':       offset,
        'genus':        genus,
        'species':      species,
        'country':      country,
        'caste':        caste  # not working
            }

    url = requests.get(url=base_url, params=arguments, timeout=(5))

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


def filter_json(json):
    """
    # Returns
        text
    """
    lst = []
    for taxaImage in json['taxaImages']:

        subfamily_name = taxaImage['subfamily']
        genus_name = taxaImage['genus']
        species_name = taxaImage['species']

        specimens = {}

        for specimen in taxaImage['specimen'][0]['images']:
            # shot_type = taxaImage['specimen'][0]['images']['shotType']
            specimens = taxaImage['specimen'][0]['images']

            for specimen in specimens:
                print(specimen)
            # if 'l' in species['specimen']['images'].value == False:
            #     print('True')


    #     new_row = [subfamily_name, genus_name, species_name]
    #     lst.append(new_row)
    # print(lst)

    # data_filtered = jmespath.search('specimens[].[catalogNumber,'
    #                                 'scientific_name, images."1".shot_types]',
    #                                 json)
    #
    # lst = []
    # for row in data_filtered:
    #     if row[2] != None:
    #         # print(row)
    #         catalog_number = row[0]
    #         scientific_name = row[1]
    #         image_url = {}
    #         if 'h' in row[2]:
    #             image_url['h'] = row[2]['h']['img'][1]
    #         if 'p' in row[2]:
    #             image_url['p'] = row[2]['p']['img'][1]
    #         if 'd' in row[2]:
    #             image_url['d'] = row[2]['d']['img'][1]
    #         for key in image_url:
    #             new_row = [catalog_number,
    #                        scientific_name, key, image_url[key]]
    #             lst.append(new_row)
    #
    # return lst

# Executing
################################################################################


# @profile
def download_to_csv(offset_set, limit_set):
    suffix = '.csv'
    input_direc = os.path.join(wd, 'data', input_dir, 'json_files')
    output_dir = os.path.join(wd, 'data', input_dir)
    nb_files = len(os.listdir(input_direc))
    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']

    offset = offset_set
    limit = limit_set
    # limit / offset = number of batches to download
    # 630976 / 9859 = 64
    check = limit - offset

    file_name = todaystr + '_formicID_db_AW.csv'
    path = '../data/'
    if not os.path.exists(path):
        os.mkdir(path)

    df2 = pd.DataFrame()

    # Obtain the max number of specimens
    nb_specimens = max_specimens(get_json(create_url(limit=1, offset=1)))
    nb_batch = 1
    total_batches = limit
    while offset < nb_specimens:
        print('Batch {} of {}: {} specimens have been checked '
              'for a total of {}'.format(
                  nb_batch, nb_specimens // limit, check, total_batches))

        nb_batch += 1
        total_batches += limit

        url = create_url(limit=limit, offset=offset)
        json = get_json(url)
        if 'empty_set' in json['specimens']:
            print("Every json batch is checked for images.")
            break
        else:
            lst = filter_json(json)
            df = create(lst)
            df2 = df2.append(df)
            offset += limit

    # replace spaces between genus and species names with underscores
    df2.replace('\s+', '_', regex=True, inplace=True)
    df2.columns = columns
    # file_path = os.path.join(path, file_name)

    df2.to_csv(os.path.join(path, file_name), index=False, header=True)


def main():
    url = create_url(
        offset = 0,
        limit = 50,
        country_set=None,
        # shot_type='h',
        genus='Pheidole')

    # print(get_url_info(url))

    if get_url_info(url) == None: # If there is no error, perform actions
        json = get_json(url)

        filter_json(json)

    else:
        print('There was a server error.')
    # download_to_csv(offset_set = 0, limit_set = 500, country='Netherlands')

if __name__ == '__main__':

################################################################################
#                                                                              #
#                                  ANTWEB API                                  #
#                                AntWeb to csv                                 #
################################################################################

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


# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset, genus, species):
    """
    # Description:
        Creation of the url to access AntWebs API, using a base_url and
        arguments

    # Input:
        limit = sets the limit for accessing specimens
        offset = sets the offset for accessing specimens
        genus = specifies the genus
        species = specifies the species

    # Returns:
        Returns an URL as response object that can be opened by the function
        request.get()

    # TODO:
        make genus and species optional
        - https://stackoverflow.com/questions/35265234/
        passing-an-optional-argument-in-a-function-python
        - https://stackoverflow.com/questions/9539921/
        how-do-i-create-a-python-function-with-optional-arguments
    """
    base_url = 'http://www.antweb.org/api/v2/?'

    arguments = {    # API arguments for in the url
        'caste':        'worker',
        'limit':        limit,
        'offset':       offset,
        # 'country':      'Netherlands',
        'genus':        genus,
        'species':      species
    }
    # Creating the AntWeb url from the base url and the API arguments
    url = requests.get(url=base_url, params=arguments)

    return url


def get_url_info(input_url):
    """
    # Description:
        Provides information on the URL

    # Input:
        input_url = the url as response object, created by create_url()

    # Returns:
        returns information on the URL
    """
    # Get basic url information
    print('URL:', input_url.url)  # does not work yet???
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))
    print('Connection status:', input_url.status_code)
    if input_url.status_code == 200:
        print('Request status: the request was fulfilled.')
    else:
        print('Request status: the request was not fulfilled.')
    print('Time elapsed to connect to URL:', input_url.elapsed)

# get JSON > database
# //////////////////////////////////////////////////////////////////////////////


def get_json(input_url):
    """
    # Description:
        Scrapes JSON files using an URL from AntWebs API

    # Input:
        input_url = the url as response object, created by create_url()

    # Returns:
        A JSON object
    """
    r = requests.get(url=input_url)
    data = r.json()
    if data == None:
        print("JSON is empty!")
    else:
        return data


def max_specimens(json):
    """
    # Description:
        View the maximum number of specimens for a JSON object.

    # Input:
        json = A JSON object

    # Returns:
        An integer of the maximum number of specimens in a JSON object.
    """
    nb_specimens = json["count"]
    return int(nb_specimens)


def filter_json(json_file):
    """
    # Description:
        Load a JSON object and filter for only relevant values.

    # Input:
        json_file = path to a JSON file

    # Returns:
        A list of lists with 4 values

    # TODO:
        combine with create() ?
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
            if 'h' in row[2]:
                image_url['h'] = row[2]['h']['img'][1]
            if 'p' in row[2]:
                image_url['p'] = row[2]['p']['img'][1]
            if 'd' in row[2]:
                image_url['d'] = row[2]['d']['img'][1]
            for key in image_url:
                new_row = [catalog_number,
                           scientific_name, key, image_url[key]]
                lst.append(new_row)

    return lst


def create(lst):
    """
    # Description:
        Creates a pandas dataframe with 4 specific column names from the list created by the filter_json() function

    # Input:
        A list of lists containing 4 items, corresponding to the columnnames

    # Returns:
        A 4 column pandas dataframe

    """
    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']
    df = pd.DataFrame(columns=columns)
    df = pd.DataFrame(lst)

    return df


def open_csv(path_to_csv):
    """
    # Description:
        This function opens a csv file and stores it in a pandas dataframe

    # Input:
        path_to_csv = The 'pathway' to a .csv file with header, seperated by comma

    # Returns:
        A pandas dataframe created from a .csv file

    # TODO:
        Fix relative / absolute pathways. What to use?
    """
    df = pd.read_csv(path_to_csv, sep=';', header=0)
    return df

# Executing
# //////////////////////////////////////////////////////////////////////////////


# @profile
def urls_to_json(csv_species, offset_set, limit_set):
    """
    # Description:
        This function downloads JSON files for a list of species and places them in a drecitory.

    # Input:
        csv_species = a csv file with 2 columns of genus and species names
        offset_set = set the offset for downloading AntWeb records in batches
        limit_set = set a limit for downloading a set of records from AntWeb

    # Returns:
        A directory of JSON files for different species

    # TODO:
        Fix pathways
        Add directory as argument
    """
    df_top101 = open_csv(csv_species)

    offset = offset_set
    limit = limit_set
    # limit / offset = number of batches to download
    # 630976 / 9859 = 64
    check = limit - offset

    path = './data/top101-JSON/'
    if not os.path.exists(path):
        os.mkdir(path)

    # Obtain the max number of specimens
    nb_specimens = df_top101.shape[0]
    nb_batch = 1
    total_batches = limit

    for index, row in tqdm(df_top101.iterrows(),
                           desc='Downloading JSON files'):

        url = create_url(
            limit=limit_set,
            offset=offset_set,
            genus=row['genus'],
            species=row['species'])

        url = url.url
        file_name = row['genus'] + '_' + row['species'] + '.json'
        species = get_json(url)
        with open(os.path.join(path, file_name), 'w') as fp:
            json.dump(species, fp)

        print('Creating URL, fechting JSON and writing to file ({} / {}).'.format(nb_batch, nb_specimens))
        nb_batch += 1
        time.sleep(0.5)


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


if __name__ == '__main__':

    # urls_to_json(
    #     csvfile='./data/2018-01-09-db-Top101imagedspecies.csv',
    #     offset_set=0,
    #     limit_set=6000
    # )

    batch_filter_to_csv(
        directory='./data/top101-JSON'
    )

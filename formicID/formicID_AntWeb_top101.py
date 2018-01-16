################################################################################
#                                                                              #
#                                  ANTWEB API                                  #
#                                 AntWeb 2 csv                                 #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function

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


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()


# Time-it function
# //////////////////////////////////////////////////////////////////////////////
# https://stackoverflow.com/questions/3620943/
# measuring-elapsed-time-with-the-time-module

#
# PROF_DATA = {}
#
#
# def profile(fn):
#     @wraps(fn)
#     def with_profiling(*args, **kwargs):
#         start_time = time.time()
#
#         ret = fn(*args, **kwargs)
#
#         elapsed_time = time.time() - start_time
#
#         if fn.__name__ not in PROF_DATA:
#             PROF_DATA[fn.__name__] = [0, []]
#         PROF_DATA[fn.__name__][0] += 1
#         PROF_DATA[fn.__name__][1].append(elapsed_time)
#
#         return ret
#
#     return with_profiling
#
#
# def print_prof_data():
#     for fname, data in PROF_DATA.items():
#         max_time = max(data[1])
#         avg_time = sum(data[1]) / len(data[1])
#         print("Function %s called %d times. " % (fname, data[0])),
#         print('Execution time max: %.3f, average: %.3f' % (max_time, avg_time))
#
#
# def clear_prof_data():
#     global PROF_DATA
#     PROF_DATA = {}


# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset, genus, species):
    """
    # Returns
        <Placeholder for notes>
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
    # Returns
        <Placeholder for notes>
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


def get_json(urllink):
    """
    Description:
        # loads the json formatted <Placeholder for notes> from the url

    # Input:
        <Placeholder for notes>

    # Returns
        Json
    """
    r = requests.get(url=urllink)
    data = r.json()
    if data == None:
        print("JSON is empty!")
    else:
        return data


def max_specimens(json):
    """
    # Returns
        <Placeholder for notes>
    """
    nb_specimens = json["count"]
    return int(nb_specimens)


def filter_json(json_file):
    """
    # Returns
        <Placeholder for notes>
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
    # Returns
        <Placeholder for notes>
    """
    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']
    df = pd.DataFrame(columns=columns)
    df = pd.DataFrame(lst)

    return df
    # print(df.head())
    # df_def = pd.DataFrame(columns=columns)
    # df_def.append(df)
    # df_def.to_csv('formicID_db_h.csv')
    # return df

    # with open('formicID_db.csv', 'a') a÷s f:
    #     for row in lst:
    #         f.write(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')

def open_csv(path_to_csv):
    df = pd.read_csv(path_to_csv, sep=';', header = 0)
    return df

# Executing
# //////////////////////////////////////////////////////////////////////////////


# @profile
def urls_to_json(offset_set, limit_set):
    """
    # Input:
        offset_set = set the offset for downloading AntWeb records in batches
        limit_set = set a limit for downloading a set of records from AntWeb

    # Description:
        this function downloads imaged only specimens with catalog number and
        scientific names into an csv file

    # Returns :
        <Placeholder for notes>
    """
    df_top101 = open_csv(
    './data/2018-01-09-db-Top101imagedspecies.csv')

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

    for index, row in df_top101.iterrows():
        url = create_url(
            limit = limit_set,
            offset = offset_set,
            genus = row['genus'],
            species = row['species'])
        url = url.url
        file_name = row['genus'] + '_' + row['species'] + '.json'
        species = get_json(url)
        with open(os.path.join(path, file_name), 'w') as fp:
            json.dump(species, fp)

        print('Creating URL, fechting JSON and writing to file ({} / {}).'.format(nb_batch, nb_specimens))
        nb_batch += 1
        time.sleep(0.5)


def batch_filter_to_csv(directory):
    df2 = pd.DataFrame()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as data_file:
                print('Filtering {}'.format(filename))
                lst = filter_json(data_file)
                df = create(lst)
                df2 = df2.append(df)

    # replace spaces between genus and species names with underscores
    df2.replace('\s+', '_', regex = True, inplace = True)
    df2.columns = [
        'catalog_number',
        'scientific_name',
        'shot_type',
        'image_url'
    ]
    # file_path = os.path.join(path, file_name)
    path = './data/top101-JSON/'
    file_name = 'top101.csv'
    df2.to_csv(os.path.join(path, file_name), index = False, header = True)
    print('All JSON files are filtered and added to the csv file.')

if __name__ == '__main__':
    # urls_to_json(offset_set=0, limit_set=6000)
    batch_filter_to_csv(directory='./data/top101-JSON')

    # @profile

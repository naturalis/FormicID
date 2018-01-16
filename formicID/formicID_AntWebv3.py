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


def create_url(limit, offset, country_set, genus):
    """
    # Returns
        text
    """
    if country_set == 'None':
        arguments = {    # API arguments for in the url
            # 'caste':        worker,
            'limit':        limit,
            'offset':       offset,
            # 'shot_type':    shot_type,
            'genus':        genus
            }
    else:
        arguments = {    # API arguments for in the url
            # 'caste':        worker,
            'limit':        limit,
            'offset':       offset,
            'country':      country_set,
            # 'shot_type':    shot_type,
            'genus':        genus
            }
    # AntWeb API v3 base url
    base_url = 'http://api.antweb.org/v3/taxaImages?'

    # Creating the AntWeb url from the base url and the API arguments
    url = requests.get(url=base_url, params=arguments, timeout=(5))

    return url


def get_url_info(input_url):
    """
    # Returns
        text
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
    return input_url.raise_for_status()

# get JSON > database
# //////////////////////////////////////////////////////////////////////////////


def get_json(urllink):
    """
    # loads the json formatted text from the url

    # Returns
        text
    """
    data = urllink.json()
    if data == None:
        print('JSON is empty!')
    else:
        print('The JSON file is loaded from the URL.')
        return data

# This function does not work for now...
# TODO: fix this function!
def max_specimens(json):
    """
    # Returns
        text
    """
    nb_specimens = json['metaData']['parameters']['specimenCount']
    print('The maximum number of specimens found are',
    '{}'.formatint(nb_specimens))
    return int(nb_specimens)


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


def create(lst):
    """
    # Returns
        text
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

# Executing
# //////////////////////////////////////////////////////////////////////////////


# @profile
def download_to_csv(offset_set, limit_set):
    """
    Input:
        offset_set = set the offset for downloading AntWeb records in batches
        limit_set = set a limit for downloading a set of records from AntWeb

    Description:
        this function downloads imaged only specimens with catalog number and
        scientific names into an csv file
    """
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
    df2.columns = [
        'catalog_number',
        'scientific_name',
        'shot_type',
        'image_url'
    ]
    # file_path = os.path.join(path, file_name)

    df2.to_csv(os.path.join(path, file_name), index=False, header=True)

if __name__ == '__main__':
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
    # @profile

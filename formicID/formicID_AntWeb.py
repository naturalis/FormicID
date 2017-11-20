###############################################################################
#                                                                             #
#                                  ANTWEB API
#                                                                             #
###############################################################################

# Packages
# /////////////////////////////////////////////////////////////////////////////
from __future__ import print_function

import requests
import json
import jmespath
import pandas as pd
import time
from functools import wraps
from urllib.request import urlretrieve
import csv
import itertools

# AntWeb basic information
# /////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset):
    """
    # Returns
        text
    """
    base_url = 'http://www.antweb.org/api/v2/?'

    arguments = {    # API arguments for in the url
        'caste':        'worker',
        'limit':        limit,
        'offset':       offset
    }
    # Creating the AntWeb url from the base url and the API arguments
    url = requests.get(url=base_url, params=arguments)

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

# get JSON > database
# /////////////////////////////////////////////////////////////////////////////


def get_json(urllink):
    """
    # loads the json formatted text from the url

    # Returns
        text
    """
    data = urllink.json()
    if data == None:
        print("JSON is empty!")
    else:
        return data


def max_specimens(json):
    """
    # Returns
        text
    """
    nb_specimens = json["count"]
    return int(nb_specimens)


def filter_json(json):
    """
    # Returns
        text
    """
    data_filtered = jmespath.search('specimens[].[catalogNumber,'
                                    'scientific_name, images."1".shot_types]',
                                    json)

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

# Time-it function
# /////////////////////////////////////////////////////////////////////////////
# https://stackoverflow.com/questions/3620943/
# measuring-elapsed-time-with-the-time-module


PROF_DATA = {}


def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in PROF_DATA:
            PROF_DATA[fn.__name__] = [0, []]
        PROF_DATA[fn.__name__][0] += 1
        PROF_DATA[fn.__name__][1].append(elapsed_time)

        return ret

    return with_profiling


def print_prof_data():
    for fname, data in PROF_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        print("Function %s called %d times. " % (fname, data[0])),
        print('Execution time max: %.3f, average: %.3f' % (max_time, avg_time))


def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}


# Executing
# /////////////////////////////////////////////////////////////////////////////
@profile
def download_to_csv(offset_set, limit_set):
    offset = offset_set
    limit = limit_set
    # 621810 / 11515 = 54
    # 621810 / 9870 = 63

    df2 = pd.DataFrame()

    nb_specimens = max_specimens(get_json(create_url(limit=1, offset=1)))

    while offset < nb_specimens:
        print("{} specimens have been checked.".format(offset))
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

    df2.columns = ['catalog_number',
                   'scientific_name', 'shot_type', 'image_url']
    df2.to_csv('./data/formicID_db_h2.csv', index=False)


@profile
def image_scrape(csvfile, start, end):
    """
    Input:
        input = path to the file.csv

    Description:
        this function scrapes images of urls in the csv file made with
        the download_to_csv function.
    """
    with open(csvfile) as images:
        images = csv.reader(images)
        start = start
        end = end
        nb_images = end - start
        for image in itertools.islice(images, start, end):
            if image[3] != 'image_url':
                urlretrieve(url=image[3], filename='./data/scrape_test/{} {} {}.jpg'.format(image[1], image[0], image[2]))
        print('{} images were downloaded.'.format(nb_images))
    #
    # for row in df['image_url']:
    #     name = (df['scientific_name']+'_'+df['catalog_number']+'.jpg')
    #     urllib.request.urlretrieve(row, str(name))


# download_to_csv(offset_set=0, limit_set=9000)
image_scrape(csvfile='./data/formicID_db_h2.csv', start=0, end=128)
print_prof_data()

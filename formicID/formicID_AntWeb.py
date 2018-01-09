################################################################################
#                                                                              #
#                                  ANTWEB API                                  #
#                                                                              #
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
import itertools
from functools import wraps
from urllib.request import urlretrieve
from tqdm import tqdm, trange


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////


# Time-it function
# //////////////////////////////////////////////////////////////////////////////
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


# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////


def create_url(limit, offset):
    """
    # Returns
        text
    """
    base_url = 'http://www.antweb.org/api/v2/?'

    arguments = {    # API arguments for in the url
        'caste':        'worker',
        'limit':        limit,
        'offset':       offset,
        'country':      'Netherlands'
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
# //////////////////////////////////////////////////////////////////////////////


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

# Executing
# //////////////////////////////////////////////////////////////////////////////
@profile
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
    # 621810 / 11515 = 54
    # 621810 / 9870 = 63
    check = limit - offset

    df2 = pd.DataFrame()

    # Obtain the max number of specimens
    nb_specimens = max_specimens(get_json(create_url(limit=1, offset=1)))

    while offset < nb_specimens:
        print("{} specimens have been checked.".format(check))
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

    # replace spaces with underscores
    df2.replace('\s+', '_', regex=True, inplace=True)

    df2.to_csv('/data/formicID_db.csv', index=False)

@profile
def image_scraper(csvfile, start, end, dir_name):
    """
    Input:
        csvfile = set the csv file to use
        start = set the starting row for downloading
        end = set the end row for downloading
        dir_name = a string of text to name the output folder, with the current
            date as prefix

    Description:
        this function scrapes images of urls found in the csv file that is made
        with the download_to_csv function.
    """
    nb_start, nb_end = start, end
    nb_images = nb_end - nb_start

    todaystr = datetime.date.today().isoformat()
    dir_name = todaystr + '_' + dir_name

    if not os.path.exists(os.path.join('../data/', dir_name)):
        os.mkdir(os.path.join('../data/', dir_name))

    with open(csvfile, 'rt') as images:
        imagereader = csv.reader(
            itertools.islice(images, nb_start, nb_end + 1))
        # nb_lines = sum(1 for row in imagereader)

        print("Starting scraping...")
        for image in tqdm(imagereader, desc='Scraping images...', total = nb_images):
            # for i in trange(nb_lines, desc='Downloading all images'):
            # for j in trange(50, desc='Downloading a set of 50 images'):

            if image[3] != 'image_url':
                filename = os.path.join('../data/', dir_name,
                '{}_{}_{}.jpg'.format(image[2], image[1], image[0]))
                urlretrieve(url = image[3], filename = filename)

        print('{} images were downloaded.'.format(nb_images))

    # for row in df['image_url']:
    #     name = (df['scientific_name']+'_'+df['catalog_number']+'.jpg')
    #     urllib.request.urlretrieve(row, str(name))

# Call scraper
# //////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    download_to_csv(offset_set=0, limit_set=9870)

    # image_scraper(
    #     csvfile = os.path.join(os.path.dirname(__file__),
    #     '../data/formicID_db_test.csv'),
    #     start = 0,
    #     end = 369,
    #     dir_name = 'scrape_netherlands')

    # print_prof_data()

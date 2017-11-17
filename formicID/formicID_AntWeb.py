###############################################################################
#                                                                             #
#                                  ANTWEB API
#                                                                             #
###############################################################################

# Packages
# /////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
# allow use of print as a function. Needed when loading in Python 2.x
import datetime
import requests
import json
import jmespath
import pandas as pd
# from PIL import Image
# import urllib.parse

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
    print('URL:', input_url.url) # does not work yet???
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
    # Returns
        text
    """
    # loads the json formatted text from the url
    data = urllink.json()
    if data = None:
        print("JSON is empty!")
    return data

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
                new_row = [catalog_number, scientific_name, key, image_url[key]]
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
# /////////////////////////////////////////////////////////////////////////////
offset_set = 0
limit_set = 11515

df2 = pd.DataFrame()
# 621810 / 11515 = 54
# 621810 / 9870 = 63

while offset_set < 621810:
    offset_set += limit_set
    print("The dataset has {} specimens.".format(offset_set))
    url = create_url(limit=limit_set, offset=offset_set)
    json = get_json(url)
    lst = filter_json(json)
    df = create(lst)
    df2 = df2.append(df)



df2.columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']
df2.to_csv('formicID_db_h.csv')


#
# AW_url = create_url(limit=15500, offset=0)
# # get_url_info(AW_url)
# # print(AW_url)
# AW_json = get_json(AW_url)
# lst = filter_json(AW_json)
# # print(lst)
# df = create(AW_json)

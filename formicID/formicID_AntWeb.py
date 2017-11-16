################################################################################
#                                                                              #
#                                  ANTWEB API                                  #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
# allow use of print as a function. Needed when loading in Python 2.x
import datetime
import requests
import json
import jmespath
# import ijson # need this?

# from PIL import Image
# import urllib
# import urllib.parse

# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////
AW_base_url = 'http://www.antweb.org/api/v2/?'

offset = 0
limit = 1000
while true:
    offset += limit

    AW_arguments = {    # API arguments for in the url
        'subfamily':    'formicinae',
        'caste':        'worker',
        #'img_type':     'h',
        'limit':         limit,
        #'country':      'netherlands',
        'offset':       offset
    }
    # with 25 limit, specimen 8 and 25 have images

    # Creating the AntWeb url from the base url and the API arguments
    AW_url = requests.get(url=AW_base_url, params=AW_arguments)


def get_url_info(input_url):
    # Get basic url information
    print('URL:', input_url.url)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))
    print('Connection status:', input_url.status_code)
    if input_url.status_code == 200:
        print('Request status: the request was fulfilled.')
    else:
        print('Request status: the request was not fulfilled.')
    print('Time elapsed to connect to URL:', input_url.elapsed)


# get_url_info(AW_url)


# Getting JSON text format from the url and put that in a dictionary
# //////////////////////////////////////////////////////////////////////////////
def get_json(input_url):
    # loads the json formatted text from the url
    AW_data = json.loads(input_url.text)
    return AW_data


AW_data_json = get_json(AW_url)


def json_filter(data):
    # filters for catalognumber, scientific_name and the images per shot_type
    data_processed = jmespath.search('specimens[].[catalogNumber,'
                                     'scientific_name, images."1".shot_types]',
                                      data)
    return data_processed


AW_name_and_image = json_filter(AW_data_json)

# print(AW_name_and_image)

lst = []
for row in AW_name_and_image:
    if row[2] != None:
        # print(row)
        catalogNumber = row[0]
        name = row[1]
        url = {}
        url['h'] = row[2]['h']['img'][1]
        url['p'] = row[2]['p']['img'][1]
        url['d'] = row[2]['d']['img'][1]
        for key in url:
            new_row = [catalogNumber, name, key, url[key]]
            lst.append(new_row)

print(lst)

df = pd.DataFrame(lst)
df.columns = ['catalogNumber', 'name', 'type', 'url']
print(df.head())


df.to_csv('pandas.csv')

with open('rows.csv', 'a') as f:
    for row in lst:
        f.write(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')

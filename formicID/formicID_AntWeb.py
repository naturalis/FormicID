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
# import urllib
# import urllib.parse

# AntWeb basic information
# /////////////////////////////////////////////////////////////////////////////


class get_url(object):
    """
    Description

    Attributes:
        subfamily:
        limit:
        offset:
    """

    def __init__(self, subfamily, limit, offset):
        """
        # Returns
            text
        """
        self.subfamily = subfamily,
        self.limit = limit,
        self.offset = offset

    def create_url(self):
        """
        # Returns
            text
        """
        base_url = 'http://www.antweb.org/api/v2/?'

        offset = self.offset
        limit = self.limit
        # while true:
        #     offset += limit
        arguments = {    # API arguments for in the url
            'subfamily':    self.subfamily,
            'caste':        'worker',
            'limit':        self.limit,
            'offset':       self.offset
        }
        # Creating the AntWeb url from the base url and the API arguments
        url = requests.get(url=base_url, params=arguments)

        return url

    # def get_url_info(self, input_url):
    #     """
    #     # Returns
    #         text
    #     """
    #     # Get basic url information
    #     print('URL:', url.url) # does not work yet???
    #     print('URL headers:', input_url.headers)
    #     print('URL type:', type(input_url.content))
    #     print('Connection status:', input_url.status_code)
    #     if input_url.status_code == 200:
    #         print('Request status: the request was fulfilled.')
    #     else:
    #         print('Request status: the request was not fulfilled.')
    #     print('Time elapsed to connect to URL:', input_url.elapsed)


# get JSON > database
# /////////////////////////////////////////////////////////////////////////////
class create_database(object):
    """
    Description

    Attributes:
        subfamily:
        limit:
        offset:

    """

    def __init__(self, urllink):
        """
        # Returns
            text
        """
        self.urllink = urllink

    def get_json(self):
        """
        # Returns
            text
        """
        # loads the json formatted text from the url
        data = formicinae_url.json()

        data_filtered = jmespath.search('specimens[].[catalogNumber,'
                                        'scientific_name, images."1".shot_types]',
                                        data)

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
    df = pd.DataFrame(lst)
    df.columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']
    # print(df.head())
    df.to_csv('formicID_db_h.csv')
    # return df

    with open('formicID_db.csv', 'a') as f:
        for row in lst:
            f.write(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')


# Executing
# /////////////////////////////////////////////////////////////////////////////
formicinae_url = get_url("formicinae", limit=1000, offset=0)
formicinae_url = formicinae_url.create_url()
# print(formicinae_url)
db = create_database(formicinae_url)
db = db.get_json()
# print(db)
create(db)

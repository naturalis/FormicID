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
# from PIL import Image
# import urllib
# import urllib.parse

# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////
AW_base_url = 'http://www.antweb.org/api/v2/?'

AW_arguments = {
    'subfamily':    'formicinae',
    'caste':        'worker',
    'img_type':     'h',
    'limit':        100,
    #'country':      'netherlands'
}

# Creating the AntWeb url from the base url and the API arguments
AW_url = requests.get(url=AW_base_url, params=AW_arguments)

# Get basic url information
def get_url_info(input_url):
    print('URL:', input_url.url)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))
    print('Connection status:', input_url.status_code)
    if input_url.status_code == 200:
        print('Request status: the request was fulfilled.')
    else:
        print('Request status: the request was not fulfilled.')
    print('Time elapsed to connect to URL:', input_url.elapsed)

get_url_info(AW_url)


# Getting JSON text format from the url and put that in a dictionary
# //////////////////////////////////////////////////////////////////////////////
def get_json(input_url):
    AW_data = json.loads(input_url.text)
    return AW_data


AW_data_json = get_json(AW_url)

AW_data_json['specimens'][7]['images']['1']['shot_types']['d'].keys()

def get_shot_types(data):
    # loop through all specimens
    for specimen in data['specimens']:

        # if the specimen has images, continue
        if 'images' in specimen:

            #only view head, profile and dorsal view
            wanted_shot_types = ['h', 'p', 'd']
            AW_images = \
            dict((k, specimen['images']['1']['shot_types'][k]) for \
            k in wanted_shot_types if \
            k in specimen['images']['1']['shot_types'])

            print(AW_images)

            #for item in AW_images['h']['img']:
            #    if 'med' in item:
            #        print(item)

get_shot_types(AW_data_json)






def print_urls(data):

    AW_dict = {}

    # loop through all specimens
    for specimen in data['specimens']:
        # if the specimen has images, continue
        if 'images' in specimen:

            # find the thumbview link for the head image
            for image_head in specimen['images']['1']['shot_types']['h']['img']:
                if "thumbview" in image_head:
                    img_head = image_head
                    print(img_head)

            # find the thumbview link for the dorsal image
            for image_dorsal in specimen['images']['1']['shot_types']['d']['img']:
                if "thumbview" in image_dorsal:
                    print(image_dorsal)

            # find the thumbview link for the profile image
            for image_profile in specimen['images']['1']['shot_types']['p']['img']:
                if "thumbview" in image_profile:
                    print(image_profile)

    for specimen in data['specimens']:
        print(specimen['scientific_name'])

    #def dict_update(dict):
    #    dict.update(self, *args)
    #    return self
    #    print(dict(AW_dict))


print_urls(AW_data_json)


################################################################################

def download_photo(self, img_url, filename):
    try:
        image_on_web = urllib.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            path = os.getcwd() + DOWNLOADED_IMAGE_PATH
            file_path = "%s%s" % (path, filename)
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False
    return True


download_photo(
    'http://www.AW.org/images/casent0005326/casent0005326_d_1_high.jpg', 'test_image.jpg')


for i in my_dict:
    print(i.get('specimens'))

"""
Wouldn’t it be awesome if you could simply do this?

for item in animals:
    print item.get("animal/type")
Note the / in the get method.

Unfortunately, this is not possible in vanilla Python, but with a really small helper class you can easily make this happen:
"""


class DictQuery(dict):
    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val


for item in my_dict:
    print(DictQuery(item).get("specimens//images/1/shot_types/p"))

#   json format     [dict]   [lst]  [dict] [dict]   [dict]    [dict][dict][lst]
image_test = (my_dict['specimens'][0]['images']
              ['1']['shot_types']['p']['img'][0:3])

print(image_test)

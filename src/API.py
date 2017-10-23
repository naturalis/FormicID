################################################################################
# API                                                                          #
################################################################################
from __future__ import print_function
# allow use of print as a function. Needed when loading in Python 2.x

import requests
import json
from PIL import Image
import urllib
import urllib.parse

AW_arguments = {
    'subfamily':    'formicinae',
    'caste':        'worker',
    'img_type':     'h',
    'limit':        25
    }
AW_base_url = 'http://www.antweb.org/api/v2/?'

AW_url = requests.get(AW_base_url, AW_arguments)

def get_url_info(input_url):
    print("URL:", input_url.url)
    print("URL headers:", input_url.headers)
    print("URL type:", type(input_url.content))
    print("Connection status:", input_url.status_code)
    if input_url.status_code == 200:
        print("Request: the request was fulfilled.")
    else:
        print("Request: the request was not fulfilled.")

    print("Time elapsed to connect to URL:", input_url.elapsed)


get_url_info(AW_url)



def get_json(input_url):
    return input_url.json()

AW_json = get_json(AW_url)

def print_urls(x):
    url_dict = {}
    for specimen in x["specimens"]:
            print(specimen.get("scientific name"))


print_urls(AW_json)


#   json format     [dict]   [lst]  [dict] [dict]   [dict]    [dict][dict][lst]
image_test = (my_dict['specimens'][0]['images']['1']['shot_types']['p']['img'][0:3])










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

download_photo('http://www.AW.org/images/casent0005326/casent0005326_d_1_high.jpg', 'test_image.jpg')


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
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val



for item in my_dict:
    print (DictQuery(item).get("specimens//images/1/shot_types/p"))

#   json format     [dict]   [lst]  [dict] [dict]   [dict]    [dict][dict][lst]
image_test = (my_dict['specimens'][0]['images']['1']['shot_types']['p']['img'][0:3])

print(image_test)

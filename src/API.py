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
# from PIL import Image
# import urllib
# import urllib.parse

# AntWeb basic information
# //////////////////////////////////////////////////////////////////////////////
AW_base_url = 'http://www.antweb.org/api/v2/?'

AW_arguments = {
    'subfamily':    'formicinae',
    'caste':        'worker',
    #'img_type':     'h',
    'limit':        8,
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

# get_url_info(AW_url)




# Getting JSON text format from the url and put that in a dictionary
# //////////////////////////////////////////////////////////////////////////////
def get_json(input_url):
    AW_data = json.loads(input_url.text)
    return AW_data

AW_data_json = get_json(AW_url)
# print(AW_data_json)


"""
def get_imaged_specimens(data):
    # loop through all specimens
    imaged_specimen_lst = []
    for specimen in data['specimens']:
        if 'images' in specimen:
            imaged_specimen_lst.append(specimen)
    return imaged_specimen_lst

AW_imaged_specimens = get_imaged_specimens(AW_data_json)
#print(AW_imaged_specimens)

AW_imaged_specimens = AW_imaged_specimens[0]
#print(AW_imaged_specimens)
AW_imaged_specimens_json = json.dumps(AW_imaged_specimens)
#print(AW_imaged_specimens_json)
"""

AW_name_plus_image = jmespath.search('"specimens"[].["catalogNumber", "scientific_name", "images"]', AW_data_json)

print(AW_name_plus_image)












"""


def get_images_urls(imaged_lst):
    image_lst = []
    wanted_shot_types = ['h', 'p', 'd']
    for x in imaged_lst[0:1]:
            AW_images = \
            dict((k, data[0]['images']['1']['shot_types'][k]) for \
            k in wanted_shot_types if \
            k in data[0]['images']['1']['shot_types'])
    return AW_images

img_lst = get_images_urls(AW_imaged_specimens)
print(img_lst)





def get_shot_types(data):
    # loop through all specimens
    for specimen in data['specimens']:

        # if the specimen has images, continue
        if 'images' in specimen:

            # creating a new dictionary
            # only view head, profile and dorsal view
            wanted_shot_types = ['h', 'p', 'd']
            AW_images = \
            dict((k, specimen['images']['1']['shot_types'][k]) for \
            k in wanted_shot_types if \
            k in specimen['images']['1']['shot_types'])
            return AW_images

image_urls = get_shot_types(AW_data_json)
print(image_urls)


def make_url_lst(data):
    url_lst = []
    for x in data:
        for item in data[x]['img']:
            if 'med' in item:
                url_lst.append(item)
    return url_lst

AW_url_lst = make_url_lst(image_urls)

print(AW_url_lst)
"""

# Downloading the images
# //////////////////////////////////////////////////////////////////////////////

"""

names = []
labels = []

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
"""


"""
{
  'url': 'http://antweb.org/api/v2/?occurrenceId=CAS:ANTWEB:14d618c',
  'catalogNumber': '14d618c',
  'family': 'formicidae',
  'subfamily': 'formicinae',
  'genus': 'Lepisiota',
  'specificEpithet': 'kgac-afr04',
  'scientific_name': 'lepisiota kgac-afr04',
  'typeStatus': '',
  'stateProvince': 'Tigray',
  'country': 'Ethiopia',
  'dateIdentified': '',
  'habitat': '',
  'minimumElevationInMeters': '912',
  'geojson': {
    'type': 'point',
    'coord': ['13.945647', '36.86088']
  },
  'images': {
    '1': {
      'upload_date': '2016-08-25 09:23:51',
      'shot_types': {
        'd': {
          'img': ['http://www.antweb.org/images/14d618c/14d618c_d_1_high.jpg', 'http://www.antweb.org/images/14d618c/14d618c_d_1_low.jpg', 'http://www.antweb.org/images/14d618c/14d618c_d_1_med.jpg', 'http://www.antweb.org/images/14d618c/14d618c_d_1_thumbview.jpg']
        },
        'l': {
          'img': ['http://www.antweb.org/images/14d618c/14d618c_l_1_high.jpg', 'http://www.antweb.org/images/14d618c/14d618c_l_1_low.jpg', 'http://www.antweb.org/images/14d618c/14d618c_l_1_med.jpg', 'http://www.antweb.org/images/14d618c/14d618c_l_1_thumbview.jpg']
        },
        'h': {
          'img': ['http://www.antweb.org/images/14d618c/14d618c_h_1_high.jpg', 'http://www.antweb.org/images/14d618c/14d618c_h_1_low.jpg', 'http://www.antweb.org/images/14d618c/14d618c_h_1_med.jpg', 'http://www.antweb.org/images/14d618c/14d618c_h_1_thumbview.jpg']
        },
        'p': {
          'img': ['http://www.antweb.org/images/14d618c/14d618c_p_1_high.jpg', 'http://www.antweb.org/images/14d618c/14d618c_p_1_low.jpg', 'http://www.antweb.org/images/14d618c/14d618c_p_1_med.jpg', 'http://www.antweb.org/images/14d618c/14d618c_p_1_thumbview.jpg']
        }
      }
    }
  }
}
"""

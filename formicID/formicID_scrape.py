################################################################################
#                                                                              #
#                                  ANTWEB API                                  #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function

import requests
import datetime
import os
import csv
import itertools
from urllib.request import urlretrieve
from tqdm import tqdm, trange


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()


# Packages
# //////////////////////////////////////////////////////////////////////////////


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

    dir_name = todaystr + '_' + dir_name

    if not os.path.exists(os.path.join('../data/', dir_name)):
        os.mkdir(os.path.join('../data/', dir_name))

    with open(csvfile, 'rt') as images:
        imagereader = csv.reader(
            itertools.islice(images, nb_start, nb_end + 1))
        # nb_lines = sum(1 for row in imagereader)

        print("Starting scraping...")
        for image in tqdm(imagereader, desc='Scraping images...', total=nb_images):
            # for i in trange(nb_lines, desc='Downloading all images'):
            # for j in trange(50, desc='Downloading a set of 50 images'):

            if image[3] != 'image_url':  # Don't scrape the header line
                filename = os.path.join('../data/', dir_name,
                                        '{}_{}_{}.jpg'.format(image[2], image[1], image[0]))
                urlretrieve(url=image[3], filename=filename)

        print('{} images were downloaded.'.format(nb_images))

    # for row in df['image_url']:
    #     name = (df['scientific_name']+'_'+df['catalog_number']+'.jpg')
    #     urllib.request.urlretrieve(row, str(name))

# Call scraper
# //////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    image_scraper(
        csvfile = os.path.join(os.path.dirname(__file__),
        '../data/formicID_db_test.csv'),
        start = 0,
        end = 30976,
        dir_name = 'scrape_netherlands')

#################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                     Scraper                                  #
#                                                                              #
################################################################################
'''
Description:
Use this script to updating the csv file for broken URLs, indet species. After that you can download all images. The images will be saved in different folders per shot type and per species.
'''

# Packages
# //////////////////////////////////////////////////////////////////////////////
import csv
import datetime
import itertools
import os
import time
from urllib.request import urlretrieve

import pandas as pd
import requests

from tqdm import tqdm

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()
wd = os.getcwd()
data_dir = os.path.join(wd, 'data')


# Make changes to the csv file
# //////////////////////////////////////////////////////////////////////////////

def csv_update(csvfile):
    """This function will remove broken links to a different csvfile and remove
    species that are indet.

    Args:
        csvfile (type): A .csv file that contains all the specimen and image information with 4 columns, namely: 'catalog_number', 'scientific_name', 'shot_type', 'image_url'

    Returns:
        type: A cleaned csv file ready for downloading.

    """
    # TODO (MJABoer):
    #     Make this function work
    #     Filter for broken links, usually containing spaces
    #     Filter for indet species
    #     Place these rows in a 'bad specimen' csv file
    csvfile = os.path.join(data_dir, csvfile)
    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']

    df_good = pd.DataFrame(columns=columns)
    df_bad = pd.DataFrame(columns=columns)

    with open(csvfile, 'rt') as r:

        reader = pd.read_csv(r, sep=';', header=0)

        for index, row in reader.itertuples():
            if ' ' in reader.loc['image_url']:
                print(row)
                df_bad.append(row)
            else:
                df_good.append(row)

    file_name_good = 'top101_good.csv'
    df_good.to_csv(os.path.join(data_dir, file_name_good), header=True)

    file_name_bad = 'top101_bad.csv'
    df_bad.to_csv(os.path.join(data_dir, file_name_good), header=True)


# Downloading of images
# //////////////////////////////////////////////////////////////////////////////

def image_scraper(csvfile, input_dir, start, end, dir_out_name):
    """This function scrapes images of urls found in the csv file that is made
    with the download_to_csv function.

    Args:
        csvfile (type): name of the csvfile
        input_dir (type): directory in FormicID/data/ that contains the csv
        start (integer): Set the starting row for downloading.
        end (integer): Set the end row for downloading.
        dir_out_name (type): a string of text to name the output folder, with
            the current date as prefix.

    Returns:
        type: A folder with images.
    """
    # Number of images that will be downloaded
    nb_images = end - start

    # The date is added to the dir_out_name
    dir_out_name = todaystr + '_' + dir_out_name

    csvfile = os.path.join(data_dir, input_dir, csvfile)

    # If the /data/'dir_out_name' directory does not exist, create one
    print('Creating folders...')
    if not os.path.exists(os.path.join(data_dir, input_dir, dir_out_name)):
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'head'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'dorsal'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'profile'))

    dir_h = os.path.join(data_dir, input_dir, dir_out_name, 'head')
    dir_d = os.path.join(data_dir, input_dir, dir_out_name, 'dorsal')
    dir_p = os.path.join(data_dir, input_dir, dir_out_name, 'profile')
    time.sleep(0.5)
    print('Folders are created')

    # Opening the csvfile from row 'start' to row 'end'
    with open(csvfile, 'rt') as images:
        imagereader = csv.reader(
            itertools.islice(images, start, end + 1))

        print("Starting scraping...")

        for image in tqdm(imagereader,
                          desc='Scraping images.',
                          total=nb_images):
            # for i in trange(nb_lines, desc='Downloading all images'):
            # for j in trange(50, desc='Downloading a set of 50 images'):

            if image[3] != 'image_url': # Don't scrape the header line

                # Create a folder for the species in a shot type folder if it
                # does not exist already, then download the image.
                if image[2] == 'h':
                    if not os.path.exists(os.path.join(dir_h, image[1])):
                        os.mkdir(os.path.join(dir_h, image[1]))
                    filename = os.path.join(dir_h, image[1],
                    '{}_{}_{}.jpg'.format(image[1], image[0], image[2]))

                    urlretrieve(url=image[3], filename=filename)

                if image[2] == 'd':
                    if not os.path.exists(os.path.join(dir_d, image[1])):
                        os.mkdir(os.path.join(dir_d, image[1]))
                    filename = os.path.join(dir_d, image[1],
                    '{}_{}_{}.jpg'.format(image[1], image[0], image[2]))

                    urlretrieve(url=image[3], filename=filename)

                if image[2] == 'p':
                    if not os.path.exists(os.path.join(dir_p, image[1])):
                        os.mkdir(os.path.join(dir_p, image[1]))
                    filename = os.path.join(dir_p, image[1],
                    '{}_{}_{}.jpg'.format(image[1], image[0], image[2]))

                    urlretrieve(url=image[3], filename=filename)

        print('{} images were downloaded.'.format(nb_images))


def main():
    # csv_update(
    #     csvfile=os.path.join(
    #         os.path.dirname(__file__),
    #         '../data/test1.csv')
    # )

    image_scraper(
        csvfile='test_5species.csv',
        input_dir='JSON-test',
        start=0,
        end=455,
        dir_out_name='test_5species_images'
    )


# main()
# //////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()

################################################################################
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
Use this script to updating the csv file for broken URLs. After that you can
download all images. The images will be saved in different folders per shot
type and per species.
'''

# Packages
# //////////////////////////////////////////////////////////////////////////////
import csv
import datetime
import itertools
import os
import re
from urllib.request import urlretrieve
from urllib.error import HTTPError

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

def csv_update(input_dir, csvfile):
    """This function will remove broken links to a different csvfile.

    Args:
        input_dir (type):
        csvfile (type): A .csv file that contains all the specimen and image
        information with 4 columns, namely: 'catalog_number',
        'scientific_name', 'shot_type' and 'image_url'.

    Returns:
        csv file: A cleaned csv file ready for downloading images.

    """
    csvfile = os.path.join(data_dir, input_dir, csvfile)

    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']

    with open(csvfile, 'rt') as csv_open:
        df = pd.read_csv(csv_open, sep=',')
        specimens = pd.DataFrame(df, columns=columns)
        specimen_blf = df[df['image_url'].str.contains('blf') == True]

        specimen_hjr = df[df['image_url'].str.contains('hjr') == True]

        frames = [specimen_blf, specimen_hjr]
        specimen_bad = pd.concat(objs=frames)

        specimen_good = pd.DataFrame(
            df[df['image_url'].str.contains('blf|hjr') == False],
            columns=columns)

        rows = []
        for row in tqdm(specimen_bad['image_url'],
                        desc='Fixing image URLs'):
            row1 = re.sub('_', '(', row, count=1)
            row2 = re.sub('_', ')', row1, count=1)
            row3 = re.sub('_', '(', row2, count=1)
            row4 = re.sub('_', ')', row3, count=1)
            rows.append(row4)
            df2 = pd.DataFrame(rows, columns=['image_url'])
        specimen_bad.update(df2)

        rows = []
        for row in tqdm(specimen_bad['catalog_number'],
                        desc='Fixing catalog numbers'):
            row1 = re.sub('_', '(', row, count=1)
            row2 = re.sub('_', ')', row1, count=1)
            rows.append(row2)
            df3 = pd.DataFrame(rows, columns=['catalog_number'])
        specimen_bad.update(df3)
        # print(specimen_bad)
        df.update(specimen_bad)
        df.to_csv(csvfile, sep=',', columns=columns, index=False)


# Downloading of images
# //////////////////////////////////////////////////////////////////////////////

def image_scraper(csvfile, input_dir, start, end, dir_out_name, update=False):
    """This function scrapes images of urls found in the csv file that is made
    with the download_to_csv function.

    Args:
        csvfile (type): name of the csvfile
        input_dir (type): directory in FormicID/data/ that contains the csv
        start (integer): Set the starting row for downloading.
        end (integer): Set the end row for downloading.
        dir_out_name (string): text to name the output folder, with the current
                               date as prefix, which is created in the
                               input_dir.
        update (Boolean): if [default=True]; the csv_update() function will be called.

    Returns:
        type: A folder with images.
    """
    if update == True:
        print('Update has been set to True. Updating file now...')
        csv_update(input_dir=input_dir,
                   csvfile=csvfile
                   )
        print('The csv file has been updated. Downloading is starting...')

    print('Update has been set to False.')
    # Number of images that will be downloaded
    nb_images = end - start

    csvfile = os.path.join(data_dir, input_dir, csvfile)

    # If the /data/'dir_out_name' directory does not exist, create one
    print('Checking Folders...')
    if not os.path.exists(os.path.join(data_dir, input_dir, dir_out_name)):
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'head'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'dorsal'))
        os.mkdir(os.path.join(data_dir, input_dir, dir_out_name, 'profile'))
        print('Folders are created')

    dir_h = os.path.join(data_dir, input_dir, dir_out_name, 'head')
    dir_d = os.path.join(data_dir, input_dir, dir_out_name, 'dorsal')
    dir_p = os.path.join(data_dir, input_dir, dir_out_name, 'profile')

    nb_rows = sum(1 for line in open(csvfile))
    print('The csv file contains {} images'.format(nb_rows))
    # Opening the csvfile from row 'start' to row 'end'
    with open(csvfile, 'rt') as images:

        imagereader = csv.reader(
            itertools.islice(images, start, end + 1))
        # nb_rows = int(sum(1 for row in imagereader))

        print('Starting scraping {} images...'.format(nb_images))

        for image in tqdm(imagereader,
                          desc='Scraping images.',
                          total=nb_images):

            if image[3] != 'image_url':  # Don't scrape the header line

                # Create a folder for the species in a shot type folder if it
                # does not exist already, then download the image.
                if image[2] == 'h':
                    if not os.path.exists(os.path.join(dir_h, image[1])):
                        os.mkdir(os.path.join(dir_h, image[1]))
                    filename = os.path.join(dir_h, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                            image[0], image[2]))

                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            print('Error 404: {}'.format(image[3]))
                            continue

                if image[2] == 'd':
                    if not os.path.exists(os.path.join(dir_d, image[1])):
                        os.mkdir(os.path.join(dir_d, image[1]))
                    filename = os.path.join(dir_d, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                            image[0], image[2]))

                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            print('Error 404: {}'.format(image[3]))
                            continue

                if image[2] == 'p':
                    if not os.path.exists(os.path.join(dir_p, image[1])):
                        os.mkdir(os.path.join(dir_p, image[1]))
                    filename = os.path.join(dir_p, image[1],
                                            '{}_{}_{}.jpg'.format(image[1],
                                            image[0], image[2]))

                    try:
                        urlretrieve(url=image[3], filename=filename)
                    except HTTPError as err:
                        if err.code == 404:
                            print('Error 404: {}'.format(image[3]))
                            continue


        print('{} images were downloaded.'.format(nb_rows))


def main():
    image_scraper(csvfile='csv_images.csv',
                  input_dir='2018-02-12-JSON-test',
                  start=0,
                  end=1500,
                  dir_out_name='images',
                  update=True
                  )

# main()
# //////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()

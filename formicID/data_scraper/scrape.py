################################################################################
#                                                                              #
#                           Scraping from csv file                             #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
import requests
import datetime
import os
import csv
import itertools
from urllib.request import urlretrieve
from tqdm import tqdm
import pandas as pd


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
todaystr = datetime.date.today().isoformat()


# Make changes to the csv file
# //////////////////////////////////////////////////////////////////////////////

def csv_update(csvfile_input):
    """
    # Description:
        This function will remove broken links to a different csvfile
        and remove species that are indet.

    # Input:
        A .csv file, created by formicID_Antweb(_...).py, that contains all the
        specimen and image information with 4 columns, namely:
            - 'catalog_number'
            - 'scientific_name'
            - 'shot_type'
            - 'image_url'

    # Returns:
        A cleaned csv file ready for downloading.

    # TODO:
        Make this function work
        Filter for broken links, usually containing spaces
        Filter for indet species
        Place these rows in a 'bad specimen' csv file
    """
    columns = [
        'catalog_number',
        'scientific_name',
        'shot_type',
        'image_url'
    ]

    df_good = pd.DataFrame(columns=columns)
    df_bad = pd.DataFrame(columns=columns)

    with open(csvfile_input, 'rt') as r:

        reader = pd.read_csv(r, sep=';', header=0)

        for index, row in reader.itertuples():
            if ' ' in reader.loc['image_url']:
                print(row)
                df_bad.append(row)
            else:
                df_good.append(row)

    path = './data/'

    file_name_good = 'top101_good.csv'
    df_good.to_csv(os.path.join(path, file_name_good), header=True)

    file_name_bad = 'top101_bad.csv'
    df_bad.to_csv(os.path.join(path, file_name_good), header=True)


# Downloading of images
# //////////////////////////////////////////////////////////////////////////////

def image_scraper(csvfile, start, end, dir_name):
    """
    # Description:
        This function scrapes images of urls found in the csv file that is made
        with the download_to_csv function.

    # Input:
        csvfile = set the csv file to use
        start = set the starting row for downloading
        end = set the end row for downloading
        dir_name = a string of text to name the output folder, with the current
            date as prefix

    # Returns
        A folder with images.

    # TODO:
        before downloading split in 3 folders for each shot_type
        put each species in it own folder in the right shot_type folder
    """

    # Number of images that will be downloaded
    nb_images = end - start

    # The date is added to the dir_name
    dir_name = todaystr + '_' + dir_name

    # If the /data/'dir_name' directory does not exist, create one
    if not os.path.exists(os.path.join('data/', dir_name)):
        os.mkdir(os.path.join('data/', dir_name))

    # Opening the csvfile from row 'start' to row 'end'
    with open(csvfile, 'rt') as images:
        imagereader = csv.reader(
            itertools.islice(images, start, end + 1))

        # Max number of lines in the csvfile
        # nb_lines = sum(1 for row in imagereader)

        print("Starting scraping...")

        # Using tqdm will add a download bar in terminal for visualizing
        # progress
        for image in tqdm(imagereader,
                          desc='Starting scraping images.',
                          total=nb_images):
            # for i in trange(nb_lines, desc='Downloading all images'):
            # for j in trange(50, desc='Downloading a set of 50 images'):

            # Don't scrape the header line
            if image[3] != 'image_url':
                filename = os.path.join('data/', dir_name,
                                        '{}_{}_{}.jpg'.format(
                                            image[1], image[0], image[2]))
                urlretrieve(url=image[3], filename=filename)

        print('{} images were downloaded.'.format(nb_images))


def main():
    csv_update(
        csvfile_input=os.path.join(
            os.path.dirname(__file__),
            '../data/test1.csv')
    )

    image_scraper(
        csvfile=os.path.join(os.path.dirname(__file__), '../data/top101.csv'),
        start=0,
        end=1,
        dir_name='top101-images'
    )


# main()
# //////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()

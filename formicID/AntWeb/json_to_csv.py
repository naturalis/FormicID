################################################################################
#                                                                              #
#                                  xxx                                 #
#                                AntWeb to csv                                 #
################################################################################
'''
Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and will then create an csv file containing a
"catalog_number", "scientific_name", "shot_type", and "image_url"
'''
# Packages
# //////////////////////////////////////////////////////////////////////////////

import json
import jmespath
import pandas as pd
import os
from tqdm import tqdm


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
wd = os.getcwd()

# Filter
# //////////////////////////////////////////////////////////////////////////////


def filter_json(json_file):
    """
    # Description:
        Load a JSON object and filter for only relevant values.

    # Input:
        json_file = a JSON object

    # Returns:
        A list of [catalog_number, scientific_name, shot_type, image_url]

    """
    json_txt = json.load(json_file)
    data_filtered = jmespath.search('specimens[].[catalogNumber,'
                                    'scientific_name, images."1".shot_types]',
                                    json_txt)

    lst = []
    for row in data_filtered:
        if row[2] != None:
            # print(row)
            catalog_number = row[0]
            scientific_name = row[1]
            image_url = {}
            # Take out urls for 'head', 'profile' and 'dorsal' shots
            if 'h' in row[2]:
                image_url['h'] = row[2]['h']['img'][1]
            if 'p' in row[2]:
                image_url['p'] = row[2]['p']['img'][1]
            if 'd' in row[2]:
                image_url['d'] = row[2]['d']['img'][1]
            for key in image_url:
                new_row = [catalog_number,
                           scientific_name, key, image_url[key]]
                lst.append(new_row)

    return lst
# Batch batch_filter_to_csv
# //////////////////////////////////////////////////////////////////////////////


def batch_json_to_csv(input_dir, output_dir, csvname):
    """
    # Description:
        From a json or batch of json files a csvfile is created with relevant
        information for downloading the images and naming the files

    # Input:
        output_dir = path and name of the output directory

    # Returns:
        Creates a .csv file in the output directory
    """
    suffix = '.csv'
    input_dir = os.path.join(wd, input_dir)
    df2 = pd.DataFrame()

    columns = ['catalog_number', 'scientific_name', 'shot_type', 'image_url']

    for filename in tqdm(os.listdir(input_dir),
                         desc='Reading JSON files'):
        if filename.endswith('.json'):
            with open(os.path.join(input_dir, filename)) as data_file:
                # print('Filtering {}'.format(filename))
                lst = filter_json(data_file)
                df = pd.DataFrame(lst, columns=columns)
                df2 = df2.append(df)

    # replace spaces between genus and species names with underscores
    df2.replace('\s+', '_', regex=True, inplace=True)
    df2.columns = columns
    # file_path = os.path.join(path, file_name)
    output_dir = os.path.join(wd, output_dir)
    df2.to_csv(os.path.join(output_dir, csvname + suffix),
               index=False, header=True)
    print('All JSON files are read, filtered and added to the csv file. \n'
          '{}{} was created in {}'.format(csvname, suffix, output_dir))


if __name__ == '__main__':
    batch_json_to_csv(
        input_dir='data/top101-JSON',
        output_dir='data/top101-JSON',
        csvname='test'
    )

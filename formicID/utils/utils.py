###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Utilitiies                                 #
#                                                                             #
###############################################################################
'''Description:
This file has code for generatl utility functions that can be used in other
scripts.
'''

# Packages
###############################################################################

# Standard library imports
import argparse
import datetime
import logging
import os

# Additional project imports
import requests

# Parameters and settings
###############################################################################


# URL info
###############################################################################
def get_url_info(input_url):
    """Provides status and information on the URL.

    Args:
        input_url (URL object): the url as response object, created by
            create_url().

    Returns:
        type: information on the URL

    """
    print('URL:', input_url.url)
    print('Connection status:', input_url.status_code)
    print('Time elapsed to connect to URL:', input_url.elapsed)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))


# Date and time stamps
###############################################################################
# YYYYMMDD
todaystr = datetime.date.today().strftime('%Y%m%d')
# YYYYMMDD_HHMMSS
today_timestr = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')


# Directory utilities
###############################################################################
wd = os.getcwd()


def create_dirs(dirs):
    """General function for creating directories..

    Args:
        dirs (list): A list of directory names..

    Returns:
        Creates directories.
    """
    try:
        for dir_ in dirs:
            if not os.path.exists(dir_):
                os.makedirs(dir_)
        return 0
    except Exception as err:
        logging.error("Creating directories error: {0}".format(err))
        exit(-1)

# Directory utilities
###############################################################################


def get_args():
    """Function for parsing arguments. For now the only argument is that the
    configuration json file has to be specified.

    Returns:
        args: returns the argument (JSON file).

    """
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-c', '--config',
        metavar='C',
        default='None',
        help='The Configuration file')
    args = argparser.parse_args()
    return args

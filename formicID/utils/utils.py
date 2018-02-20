################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Utilitiies                                  #
#                                                                              #
################################################################################
'''
Description:
This file has code for utility functions that can be used in other scripts.
'''

# Packages
################################################################################

# Parameters and settings
################################################################################


# URL info
################################################################################
def get_url_info(input_url):
    """Provides status and information on the URL.

    Args:
        input_url (type): the url as response object, created by create_url().

    Returns:
        type: information on the URL
    """
    print('URL:', input_url.url)
    print('Connection status:', input_url.status_code)
    print('Time elapsed to connect to URL:', input_url.elapsed)
    print('URL headers:', input_url.headers)
    print('URL type:', type(input_url.content))

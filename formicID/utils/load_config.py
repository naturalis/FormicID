###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Utilitiies                                 #
#                                    Config                                   #
###############################################################################
"""Description:
This script will read the config.json file from the configs folder. The json
file contains settings for running experiments.
"""
# Packages
###############################################################################

# Standard library imports
import os

# Data tools imports
import json

# Additional project imports
from bunch import Bunch

# Load and process config
###############################################################################


def _get_config_from_json(json_file):
    """Get the config from a json file.

    Args:
        json_file (JSON object): The JSON configuration.

    Returns:
        Bunch object: the configuration as a Bunch object.
        dict: the configuration as a dictionary.

    """
    # parse the configurations from the config json file provided
    with open(json_file, "r") as config_file:
        config_dict = json.load(config_file)
    # convert the dictionary to a namespace using bunch lib
    config = Bunch(config_dict)
    return config, config_dict


def process_config(jsonfile):
    """Processing the configuration JSON for the creating the directory paths.

    Args:
        jsonfile (JSON object): The JSON configuration file.

    Returns:
        Bunch object: the JSON configuration Bunch object.
    """
    config, _ = _get_config_from_json(jsonfile)
    config.summary_dir = os.path.join(
        "experiments", config.exp_name, "summary"
    )
    config.checkpoint_dir = os.path.join(
        "experiments", config.exp_name, "checkpoint"
    )
    return config

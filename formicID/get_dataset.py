###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                Get species list                             #
#                                                                             #
###############################################################################
"""Description:

"""

# Packages
###############################################################################
from utils.load_config import process_config
from utils.utils import get_args
from data_loader.data_input import split_in_directory
from data_scraper.scrape import get_dataset
from data_loader.data_input import remove_reproductives

# Main code
###############################################################################
try:
    args = get_args()
    config = process_config(args.config)
except:
    logging.error("Missing or invalid arguments.")
    exit(0)

# Creating a dataset
###############################################################################
# TODO: Automatically create species_json
# get_dataset(
#     input="testall.csv",
#     n_jsonfiles=100,
#     config=config,
#     shottypes="hdp",
#     quality="medium",
#     update=True,
#     offset_set=0,
#     limit_set=99999,
# )

# split into training, validation and test
###############################################################################
# split_in_directory(config=config, bad="data/badspecimens_p.csv")

# Remove reproductives from dataset
###############################################################################
remove_reproductives(
    csv="data/reproductives.csv",
    dataset="top97species_Qmed_def_clean_wtest",
    config=config,
)

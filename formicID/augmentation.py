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

# FormicID imports
from utils.img import save_augmentation
from utils.img import show_dataset
from utils.load_config import process_config
from utils.utils import create_dirs
from utils.utils import get_args

# Main code
###############################################################################
try:
    args = get_args()
    config = process_config(args.config)
except:
    logging.error("Missing or invalid arguments.")
    exit(0)

create_dirs([config.summary_dir, config.checkpoint_dir])

save_augmentation(
    image="data/top97species_Qmed_def_clean/images/head/1-training/eciton_burchellii/eciton_burchellii_casent0009221_h.jpg",
    config=config,
    show=True,
)

# show_dataset(
#     image_dir="data/top97species_Qmed_def_clean/images",
#     config=config,
#     max_img=32,
#     n_cols=4,
#     # save="dataset_example.png",
# )

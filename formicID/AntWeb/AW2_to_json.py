###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                 ANTWEB API v2                               #
#                                AntWeb to json                               #
###############################################################################
"""Description:
This script requires the use of an csv file with 2 columns, filled with a genus
and a species name. The script will go over the csv file and download a json
file for this genus+species and places the JSON file in a folder.
"""
# Packages
###############################################################################

# Standard library imports
import logging
import os
import sys
import time
from itertools import islice
from urllib.error import HTTPError
from urllib.request import urlopen
import re

# Data tools imports
import json
import pandas as pd
from csv import Sniffer

# Additional project imports
import requests
from tqdm import tqdm



# Extract most imaged species from AntWeb
###############################################################################

def _get_species_name_from_line(htmlline):
    a = "?genus="
    b = "&species="
    genus = htmlline.split(a)[-1].split(b)[0]
    c = "species="
    d = "&rank="
    species = htmlline.split(c)[-1].split(d)[0]
    return genus, species

# <div class="list_extras images"><a href="https://www.antweb.org/images.do?genus=acanthognathus&amp;species=rudis&amp;rank=species&amp;project=allantwebants"><span class="numbers">4</span> Images</a></div>



def _get_relevant_lines_from_html(url, min_images):
    htmldata = requests.get(url)
    htmldata.text
    lines = []
    string = "list_extras images"
    for line in tqdm(htmldata.iter_lines(decode_unicode='utf-8'), desc="Reading HTML lines", unit=" lines"):
        if line:
            if string in line:
                if re.findall('\d+', line):
                    nb_images = int(re.search(r'\d+', line).group())
                    if nb_images >= min_images:
                        lines.append(line)
    return lines

def most_imaged_species_to_csv(output, min_images=100):
    """
    these scripts work, problem is that some specimens have lots of close-up pictures, e.g. for genetelia (see https://www.antweb.org/specimenImages.do?name=antweb1008499&project=allantwebants)
    """
    url = "https://www.antweb.org/taxonomicPage.do?rank=species&project=allantwebants&statusSetSize=max&statusSet=valid%20extant&statusSet=typed"
    relevant_lines = _get_relevant_lines_from_html(url, min_images)
    # print(relevant_lines)
    rows = []
    for line in relevant_lines:
        nb_images = int(re.search(r'\d+', line).group())
        genus, species  = _get_species_name_from_line(line)
        row = [genus, species, nb_images]
        rows.append(row)
    df = pd.DataFrame(rows, columns=("genus", "species", "nb_images"))
    df.to_csv(os.path.join("data", output), sep=",", index=False)


# Creating an URL
###############################################################################


def _create_url(limit, offset, **kwargs):
    """Creation of the url to access AntWebs API V2, using a base_url and
    arguments.

    Args:
        limit (int): sets the limit for accessing specimens.
        offset (int): sets the offset for accessing specimens.

    **Kwargs:
        genus (str): specifies the genus.
        species (str): specifies the species.
        country (str): specifies the country.
        caste (str): specifies the caste (does not work in API v2).

    Returns:
        URL object: Returns an URL as response object that can be opened by the
        function `request.get()`.

    Raises:
        TypeError: In case of an invalid kwarg.

    """
    allowed_kwargs = {"genus", "species", "country", "caste"}
    for k in kwargs:
        if k not in allowed_kwargs:
            raise TypeError(
                "Unexpected keyword argument passed to "
                "_create_url: {}".format(str(k))
            )

    genus = kwargs.get("genus", None)
    species = kwargs.get("species", None)
    country = kwargs.get("country", None)
    caste = kwargs.get("caste", None)
    base_url = "http://www.antweb.org/api/v2/?"
    arguments = {
        "limit": limit,
        "offset": offset,
        "genus": genus,
        "species": species,
        "country": country,
        "caste": caste,  # not working
    }
    url = requests.get(url=base_url, params=arguments)
    return url


# Download JSON files from URLs
###############################################################################


def _get_json(input_url):
    """Scrapes JSON files from AntWeb URLs.

    Args:
        input_url (URL object): an URL containing a JSON object.

    Returns:
        JSON: A JSON object.

    Raises:
        AssertionError: If the json object contains nothing.

    """
    r = requests.get(url=input_url)
    data = r.json()
    if data != None:
        return data

    else:
        raise AssertionError(
            "There is no JSON data in the url: {0}.".format(input_url.url)
        )


def urls_to_json(
    csv_file, dataset_name, n_jsonfiles=None, offset_set=0, limit_set=9999
):
    """This function downloads JSON files for a list of species and places them
    in a drecitory. An limit_set higher than 10,000 will usually create
    problems if no species and genus is provided. If you get HTTP ERROR 500
    you will probably need to set the limit lower.

    Args:
        csv_file (str): The csv file with genus and species names.
        dataset_name (str): Name for the dataset, and also for naming the
            directory that will hold this dataset. The JSON files will be
            saved here.
        offset_set (int): The offset for downloading AntWeb records in
            batches. Defaults to `0`.
        limit_set (int): The limit for downloading a set of AntWeb records.
            Defaults to `9999`.

    Returns:
        A directory of JSON files for different species.

    Raises:
        ValueError: If `limit_set` is > 12,000.
        AssertionError: If `csv_file` is not a .csv file.
        AssertionError: If the csv file is not comma delimited.
        AssertionError: When the .csv does not have 2 columns.
        AssertionError: When the columns are not named correctly; `genus` and
            `species`.

    """
    nb_indet = 0
    nb_invalid = 0
    attempts = 5
    # if limit_set > 12000:
    #     raise ValueError('The `limit_set` should be lower than 12,000.')
    output_dir = os.path.join("data", dataset_name, "json_files")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if csv_file.endswith(".csv") == True:
        csv_file = os.path.join("data", csv_file)
    else:
        raise AssertionError(
            "{0} is not in the correct format of `.csv`.".format(csvfile)
        )

    logging.info(
        "Reading {0} and creating json_files folder.".format(csv_file)
    )
    with open(csv_file, "rt") as csv_open:
        dialect = Sniffer().sniff(csv_open.readline(), [",", ";"])
        csv_open.seek(0)
        if dialect.delimiter == ";":
            raise AssertionError(
                "Please us a comma (,) delimited csv file ",
                "instead of {0}.".format(dialect.delimiter),
            )

        csv_df = pd.read_csv(csv_open, sep=",")
        if len(csv_df.columns) != 2:
            raise AssertionError(
                "The `.csv` should only have 2 column ",
                "instead of {0} column(s).".format(len(csv_df.columns)),
            )

        if csv_df.columns.tolist() != ["genus", "species"]:
            raise AssertionError(
                "The columns are not correctly named: "
                "{} and {}. The column headers should be "
                "column 1: `genus` and column 2: "
                "`species`.".format(csv_df.columns.tolist())
            )

        for index, row in csv_df.iterrows():
            if row["species"] == "indet":
                nb_indet += 1
        logging.info(
            "{0} indet species found and will be skipped from "
            "downloading.".format(nb_indet)
        )
        nb_specimens = csv_df.shape[0] - nb_indet
        if n_jsonfiles is not None:
            nb_specimens = n_jsonfiles

        for index, row in tqdm(
            islice(csv_df.iterrows(), 0, n_jsonfiles),
            total=nb_specimens,
            desc="Downloading species JSON files",
            unit="Species",
        ):
            url = _create_url(
                limit=limit_set,
                offset=offset_set,
                genus=row["genus"],
                species=row["species"],
            )
            # Skip `indet` species:
            if row["species"] == "indet":
                logging.info('Skipped: "{}".'.format(url.url))
            # Download `non-indet` species:
            else:
                logging.info("Downloading JSON from: {0}".format(url.url))
                file_name = row["genus"] + "_" + row["species"] + ".json"
                for attempt in range(attempts):
                    try:
                        species = _get_json(url.url)
                        if species["count"] > 0:
                            # TODO: fix line below. Stops checking after 2
                            # json files are present.
                            if not os.path.isfile(
                                os.path.join(output_dir, file_name)
                            ):
                                with open(
                                    os.path.join(output_dir, file_name), "w"
                                ) as jsonfile:
                                    json.dump(species, jsonfile)
                            else:
                                logging.info(
                                    "JSON file for {0} {1} already exists "
                                    "and will not be downloaded "
                                    "again.".format(
                                        row["genus"], row["species"]
                                    )
                                )
                                return

                        # If server returns species with 0 specimen count:
                        if species["count"] == 0:
                            nb_invalid += 1
                            logging.info(
                                '"{0} {1}" has {2} records or does not '
                                "exist as a valid species".format(
                                    row["genus"],
                                    row["species"],
                                    species["count"],
                                )
                            )

                    except HTTPError as e:
                        print(e)
                    else:
                        break

                else:
                    logging.debug(
                        "For {0} attempts the server did not respond for "
                        "URL: {1}".format(attempts, url.url)
                    )
    nb_downloaded = n_jsonfiles - nb_invalid
    logging.info(
        "Downloading is finished. {} JSON files have been "
        "downloaded. With {} invalid name(s).".format(
            nb_downloaded, nb_invalid
        )
    )

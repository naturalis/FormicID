# FormicID

_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.com/naturalis/FormicID.svg?token=1cLc3spsoyrFkzth95Ho&branch=master)](https://travis-ci.com/naturalis/FormicID) · [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/naturalis/FormicID/graphs/commit-activity) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/issues/) · [![](https://img.shields.io/github/issues-closed-raw/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues?q=is%3Aissue+is%3Aclosed)

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:1 -->

-   [FormicID](#formicid)
	- [Description](#pencil-description)
		- [Proposal](#blacknib-proposal)
	- [How to use](#arrowforward-how-to-use)
	- [Project Structure](#bookmark-project-structure)
	- [AntWeb](#ant-antweb)
		- [AntWeb API](#satellite-antweb-api)
		- [Images / Dataset](#openfilefolder-images-dataset)
	- [Neural Network](#computer-neural-network)
		- [Ready to use models](#mag-ready-to-use-models)
		- [Self-made model](#triangularruler-self-made-model)
	- [Requirements](#clipboard-requirements)
	- [Credits](#scroll-credits)
	- [Why this name, FormicID?](#exclamation-why-this-name-formicid)

<!-- /TOC -->

## :pencil: Description

Code repository for CNN-based image classification of AntWeb images

![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)

### :black_nib: Proposal

The proposal can be found [here](https://github.com/naturalis/FormicID-proposal).

## :arrow_forward: How to use

### Step 1 - Get the code

Clone the repository

```sh
$ git clone https://github.com/naturalis/FormicID
$ cd ./FormicID
```

### Step 2 - Downloading the data
_Skip step 2 if you don't need to download the data._

#### Step 2.1 - Which species

Create a 2 column csv file with the genus+species you want to download from AntWeb as follows:

| genus  | species  |
| ------ | -------- |
| genus1 | species1 |
| genus2 | species2 |
| ...    | ...      |

#### Step 2.2 - Get the species information

With the `urls_to_json()` function uncommented will download all the JSON objects for your species, but it will ignore `indet` species if these are in the csv file. Set the following settings in `urls_to_json`:

-   `csv_file`: csvfile name
-   `input_dir`: input directory
-   `output_dir`: output directory
-   `offset_set`: offset
-   `limit_set`: limit

#### Step 2.3 - Format the species information

With `batch_json_to_csv()` function uncommented will create a csv file with the relevant information for downloading and naming images correctly to the output folder. Set the following settings in `batch_json_to_csv`):

-   `input_dir`: input directory
-   `output_dir`: output directory
-   `csvname`: csv name for the new csv

#### Step 2.4 - Download the images

Uncommenting the `image_scraper()` function will download the images to the output folder. The csv file from step 3 could contain some unvalid URLs and these will be repaired if you flag `image_scraper(update=True)`. This will repair broken URls (usually from `blf` or `hjr` collections because AntWebs API changes `(` and `)` to `_`). After updating the csv, the script will start downloading images and will put these in newly created folders for head, dorsal and profile shots. In these folders, every species is put in its own folder. Set the following settings in `image_scraper()`:

-   `csvfile`: csv file from step 3
-   `input_dir`: input_dir directory of the csv file
-   `start`: start number (line where to start in the csv file)
-   `end`: end number (line where to end in the csv file)
-   `output_dir_name`: directory name for the images
-   `update`: update (whether to update the csv file for broken urls or not)

### Step 3 - Configuration

Configure `formicID/configs/config.json`
- Give the experiment a name.
- Set the number of epochs, batch_size, learning rate, iterations per epoch, seed
- Set the model to one of the Keras model applications that can be loaded from `models/models.py`;
  - 'InceptionV3'
  - 'Xception',
  - 'Resnet50'
  - 'DenseNet169'

_Later more..._

```json
{
    "exp_name": "test1",
    "num_epochs": 5,
    "num_iter_per_epoch": 10,
    "learning_rate": 0.001,
    "batch_size": 10,
    "state_size": [784],
    "max_to_keep": 5,
    "dropout": 0.5,
    "optimizer": "Nadam",
    "model": "InceptionV3",
    "seed": 1
}
```

### Step 7 - Running the model

Now you can run `formicID/main.py` with `config.json` as argument and the data will be downloaded, split, and prepared, so the network can train. The trainier is loaded from `trainers/train.py`.

### Additional
Utilities that can be used are:
- Saving examples of data augmentation
- Visualizing a few of images in a plot
- Handeling models (e.g. saving, loading, visualizing, etc.)
- _More coming later_

_To be continued_

## :bookmark: Project Structure

    |-- formicID
        |-- __init__.py
        |-- main.py
        |-- AntWeb
        |   |-- __init__.py
        |   |-- AW2_to_json.py
        |   |-- AW3_to_json.py    
        |   |-- json_to_csv.py
        |-- configs
        |   |-- config.json
        |-- data_loader
        |   |-- __init__.py
        |   |-- data_input.py
        |-- data_scraper
        |   |-- __init__.py
        |   |-- scrape.py
        |-- mains
        |   |-- __init__.py
        |-- models
        |   |-- __init__.py
        |   |-- build.py
        |   |-- models.py
        |-- testers
        |   |-- __init__.py
        |   |-- tester.py
        |-- trainers
        |   |-- __init__.py
        |   |-- train.py
        |-- utils
            |-- __init__.py
            |-- img.py
    		|-- load_config.py
    		|-- logger.py
    		|-- model_utils.py
    		|-- utils.py

## :ant: AntWeb

> AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.
>
> Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.

_Text from Antweb.org_

### :satellite: AntWeb API

Images are harvested from [`www.AntWeb.org`](www.antweb.org). At this moment version 2 is used because version 3 was not released when the project started. Version 3 is also still in beta. Later, the scripts will be changed to use version 3.

-   [AntWeb API version 2](https://www.antweb.org/api/v2/)
-   [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

### :open_file_folder: Images / Dataset

Below you can see two images representing the dataset. One is an image of _Lasius flavus_ and the other one is a mosaic of _Tetramorium gollum_ I made using the image set.

| _Lasius flavus_                                                                      | Mosaic of _Tetramorium gollum_                                                 |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| ![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true) | ![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true) |

## :computer: Neural Network

### :mag: Ready to use models

-   Inception v3 (recommended)
-   Xception
-   ResNet
-   DenseNet

### :triangular_ruler: Self-made model

It will also be possible to use a model made by the author.

## :clipboard: Requirements

-   [Keras | Why use Keras?](https://keras.io/why-use-keras/)
-   [Requirements](requirements.txt)

## :scroll: Credits

-   Naturalis Biodiversity Center
-   Supervisor: dr. Rutger Vos
-   2nd Corrector: dr. Jeremy Miller
-   [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

## :exclamation: Why this name, FormicID?

FormicID is a concatenation of Formicidae (the family name of ants) and identification

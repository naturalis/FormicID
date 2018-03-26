# FormicID

_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.org/naturalis/FormicID.svg?branch=master)](https://travis-ci.org/naturalis/FormicID) · [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · 
[![GitHub commit activity the past week, 4 weeks, year](https://img.shields.io/github/commit-activity/y/eslint/eslint.svg)](https://github.com/naturalis/FormicID) · [![GitHub contributors](https://img.shields.io/github/contributors/cdnjs/cdnjs.svg)](https://github.com/naturalis/FormicID) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues)


<!-- TOC depthFrom:1 depthTo:2 withLinks:1 updateOnSave:0 orderedList:0 -->

- [FormicID](#formicid)
- [Description](#pencil-description)
  - [Proposal](#blacknib-proposal)
- [How to use](#arrowforward-how-to-use)
  - [Step 1 - Get the code](#step-1-get-the-code)
  - [Step 2 - Downloading the data](#step-2-downloading-the-data)
  - [Step 3 - Configuration](#step-3-configuration)
  - [Step 4 - Model initialisation and training](#step-4-model-initialisation-and-training)
  - [Step 5 Evaluation](#step-5-evaluation)
  - [Additional](#additional)
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

# :pencil: Description

Code repository for CNN-based image classification of AntWeb images

![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)

## :black_nib: Proposal

The proposal can be found [here](https://github.com/naturalis/FormicID-proposal).

# :arrow_forward: How to use

## Step 1 - Get the code

Clone the repository

```sh
$ git clone https://github.com/naturalis/FormicID
$ cd ./FormicID
```

## Step 2 - Downloading the data

_Skip step 2 if you don't need to download the data._

### Step 2.1 - Which species

Create a 2 column csv file with the genus+species you want to download from AntWeb as follows:

genus  | species
------ | --------
genus1 | species1
genus2 | species2
...    | ...

## Step 2.2 - Get the species information

Uncomment the `urls_to_json()` function. This will download all the JSON objects for your species, but it will ignore `indet` species if these are in the csv file (because this is not a set of real species). Set the following arguments in `urls_to_json`:

- `csv_file`: csvfile name
- `input_dir`: input directory
- `output_dir`: output directory
- `offset_set`: offset
- `limit_set`: limit

## Step 2.3 - Format the species information

Uncomment the `batch_json_to_csv()` function. This will create a csv file with the relevant information for downloading and naming images correctly to the output folder. Set the following arguments in `batch_json_to_csv`):

- `input_dir`: input directory
- `output_dir`: output directory
- `csvname`: csv name for the new csv

## Step 2.4 - Download the images

Uncomment the `image_scraper()` function. This will download the images to an output folder, split by shottype, and then by species.

> The csv file from step 2.3 could contain some unvalid URLs and these will be repaired if you flag `image_scraper(update=True)`. This will repair broken URls (usually from `blf` or `hjr` collections because AntWebs API changes `(` and `)` to `_`).

Set the following settings in `image_scraper()`:

- `csvfile`: csv file from step 2.3
- `input_dir`: input_dir directory of the csv file
- `start`: start number (line where to start in the csv file)
- `end`: end number (line where to end in the csv file)
- `output_dir_name`: directory name for the images
- `update`: update (whether to update the csv file for broken urls or not)

## Step 3 - Configuration

Configure `formicID/configs/config.json`
- Give the experiment a name.
- Set the number of `epochs`, `iterations per epoch`, `learning rate`, `batch size`, `dropout` and `seed`
- Set the `model` to one of the Keras model applications that can be loaded from `models/models.py`:
  - `InceptionV3`
  - `Xception`
  - `Resnet50`
  - `DenseNet169`
  - `Build` (this is the own designed network)
- Set the `optimizer` to one of the following:
  - `Nadam`
  - `Adam`
  - `RMSprop`
  - `SGD`

```json
{
    "exp_name": "test1",
    "num_epochs": 5,
    "num_iter_per_epoch": 10,
    "learning_rate": 0.001,
    "batch_size": 10,
    "dropout": 0.5,
    "optimizer": "Nadam",
    "model": "InceptionV3",
    "seed": 1
}
```

## Step 4 - Model initialisation and training

Now you can run `formicID/main.py` with `config.json` as argument and the data will be downloaded, split, and prepared using the `load_data()` function from `data_loader/data_input.py` where the shottype can be specified. Then the model will be loaded that is specified in the configuration file. The trainer is loaded from `trainers/train.py` and training will begin.

## Step 5 Evaluation

After training it will be possible to launch TensorBoard to view loss, accuracy, and RMSE for training and validation. Further callbacks are `EarlyStopping` and `ModelCheckpoint`. Callbacks are loaded from `utils/logger.py`

## Additional

Utilities that can be loaded are:

- Saving examples of data augmentation (`utils/img.py`)
- Visualizing a few of images in a plot (`utils/img.py`)
- Handeling models (e.g. saving, loading, visualizing, etc.) (`utils/model_utils.py`)
- Training on multiple GPUs (`utils/model_utils.py`)
- The `utils/load_config.py` is for reading the configuration file from step 3.
- `utils/utils.py` has general utility functions and variables.
- _More coming later_

_To be continued_

# :bookmark: Project Structure

```
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
```

# :ant: AntWeb

> AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.

> Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.

_Text from Antweb.org_

## :satellite: AntWeb API

Images are harvested from [`www.AntWeb.org`](www.antweb.org). At this moment version 2 is used because version 3 was not released when the project started. Version 3 is also still in beta. Later, the scripts will be changed to use version 3.

- [AntWeb API version 2](https://www.antweb.org/api/v2/)
- [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

## :open_file_folder: Images / Dataset

Below you can see two images representing the dataset. One is an image of _Lasius flavus_ and the other one is a mosaic of _Tetramorium gollum_ I made using the image set.

| _Lasius flavus_ | Mosaic of _Tetramorium gollum_ |
|----------------------------------- | ----------------------------------|
|![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true) | ![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true)|

# :computer: Neural Network

## :mag: Ready to use models

- Inception v3 (recommended)
- Xception
- ResNet
- DenseNet

## :triangular_ruler: Self-made model

It will also be possible to use a model made by the author.

# :clipboard: Requirements

- [Python3 (3.6)](https://www.python.org/downloads/release/python-364/) 
- [Keras | Why use Keras?](https://keras.io/why-use-keras/)
- [Requirements](requirements.txt)

# :scroll: Credits

- Naturalis Biodiversity Center
- Supervisor: dr. Rutger Vos
- 2nd Corrector: dr. Jeremy Miller
- [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

# :exclamation: Why this name, FormicID?

FormicID is a concatenation of Formicidae (the family name of ants) and identification

# FormicID

_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.org/naturalis/FormicID.svg?branch=master)](https://travis-ci.org/naturalis/FormicID) · [![Docker Build Status](https://img.shields.io/docker/build/jrottenberg/ffmpeg.svg)](https://hub.docker.com/r/marijnjaboer/formicid-auto/) · [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/naturalis/FormicID/graphs/commit-activity) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues) · [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)



<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [FormicID](#formicid)
- [Description](#description)
	- [Proposal](#proposal)
- [How to use](#how-to-use)
	- [Step 1 - Get the code](#step-1-get-the-code)
	- [Step 2 - Downloading the data](#step-2-downloading-the-data)
	- [Step 3 - Configuration](#step-3-configuration)
	- [Step 4 - Model initialisation and training](#step-4-model-initialisation-and-training)
	- [Step 5 - Evaluation](#step-5-evaluation)
	- [Step 6 - Optional](#step-6-optional)
- [Project Structure](#project-structure)
- [AntWeb](#antweb)
	- [AntWeb API](#antweb-api)
	- [Images / Dataset](#images-dataset)
- [Neural Network](#neural-network)
	- [Ready to use models](#ready-to-use-models)
	- [Self-made model](#self-made-model)
- [Requirements](#requirements)
- [Credits](#credits)
- [Why this name, FormicID?](#why-this-name-formicid)

<!-- /TOC -->

# Description

Code repository for CNN-based image classification of AntWeb images

![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)

## Proposal

The proposal can be found [here](https://github.com/naturalis/FormicID-proposal).

# How to use

## Step 1 - Get the code

Clone the repository

```sh
$ git clone https://github.com/naturalis/FormicID
$ cd ./FormicID
```

## Step 2 - Downloading the data

_Skip step 2 if you don't need to download the data._

Create a 2 column .csv file with the genus + species specified for downloading from AntWeb. `indet` species will be skipped because it it just a aggregation of unidentified specimens within a genus. Species that will show `0` specimen count will also be skipped.

genus  | species
------ | --------
genus1 | species1
genus2 | species2
...    | ...

Next, set the correct values for the function below. This function will download json files that will hold all the information on species (such as names, catalog identifier and URLs to images). Then it will filter out the relevant information for downloading and naming the images, after which it will download the images. Quality of images is one of: `low`, `medium`, `thumbview` or `high`.

```python
get_dataset(
    input='species.csv',    # The csv file from step `2.1.
    n_jsonfiles=5,          # Set a max number of JSON files to download.
    config=config,          # The configuration file.
    quality='low',          # The quality of images.
    update=True,            # Whether to update for broken URLs.
    offset_set=0,           # The offset for specimens in a JSON file.
    limit_set=9999          # The specimen limit in a JSON file.
)
```

## Step 3 - Configuration

Configure `formicID/configs/config.json`
- Give the experiment a name.
- Set a dataset to use.
- Set the following (as integers):
  - `epochs`
  - `learning rate`
  - `batch size`
  - `dropout`
  - `seed`
- Set the `model` to one of:
  - `InceptionV3`
  - `InceptionResNetV2`
  - `Xception`
  - `Resnet50`
  - `DenseNet169`
  - `Build` (this is the own designed network)
- Set the `optimizer` to one of the following:
  - `Nadam`
  - `Adam`
  - `RMSprop`
  - `SGD`
  - `Eve`
- Set the `test_split` and `val_split` percentages as float.
- Set the `shottype` to use (`dorsal`, `head` or `profile`).
- The prelast Dense Layer activation: `"relu"` or `PReLU`
```json
{
    "exp_name": "experiment_name",
    "data_set": "dataset_name",
    "batch_size": 32,
    "dropout": 0.5,
    "learning_rate": 0.001,
    "model": "InceptionV3",
    "num_epochs": 100,
    "num_iter_per_epoch": 32,
    "optimizer": "Nadam",
    "seed": 1,
    "test_split": 0.1,
    "val_split": 0.2,
    "shottype": "head"
}
```

## Step 4 - Model initialisation and training

Now you can run `formicID/main.py` with `config.json` as system argument and the data will be downloaded, split, and prepared. Then the model will be initialized, compiled and trained.

## Step 5 - Evaluation

After training it will be possible to launch TensorBoard to view loss, accuracy, and top-3 accuracy for training and validation. Using `evaluator()` the test set could be run against the model to see test metrics.

Possible callbacks, loaded using `utils/logger.py`, are `EarlyStopping`, `ModelCheckpoint`, `CSVLogger` and `ReduceLROnPlateau`.

Further evaluation options are:
- It is possible to plot these metrics using `plot_history()`.  
- Predict labels for the test set using `predictor()`.
- Predict the label for a URL retrieved image using `predict_image_from_url()`.
- Plot a confusion matrix using the species names, true labels and predicted labels using `plot_confusion_matrix()`.

## Step 6 - Optional

Utilities that can be loaded are:
- Image utilities
  - Saving data augmentation examples of 1 sample image `save_augmentation()`.
  - Viewing data augmentation for 1 sample images  `show_augmentation_from_dir()`.
  - Viewing a few images `show_multi_imgimg()`.
- Handeling models and weights.
  - Saving a model `save_model()`.
  - Loading a model from a file `load_model_from_file()`.
  - Saving weights `weights_load()`.
  - Model summary `model_summary()`.
  - Saving a models as configuation file `model_config()`.
  - Load a model from a configuration file `model_from_config()`.
  - Load a model from a JSON file `model_from_architecture()`.
  - Visualize the model `model_visualization()`.
  - Train multiple GPUs `make_multi_gpu()`.
- _More coming later_


# Project Structure

```
|-- formicID
    |-- main.py
    |-- AntWeb
    |   |-- AW2_to_json.py
    |   |-- AW3_to_json.py    
    |   |-- json_to_csv.py
    |-- configs
    |   |-- config.json
    |-- data_loader
    |   |-- data_input.py
    |-- data_scraper
    |   |-- scrape.py
    |-- models
    |   |-- build.py
    |   |-- models.py
    |-- testers
    |   |-- tester.py
    |-- trainers
    |   |-- train.py
    |-- utils
        |-- img.py
        |-- load_config.py
        |-- logger.py
        |-- model_utils.py
        |-- utils.py
```

# AntWeb

> AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.

> Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.

_Text is taken from [www.AntWeb.org](www.antweb.org)_

## AntWeb API

Images are harvested from [www.AntWeb.org](www.antweb.org). At this moment version 2 is used because version 3 was not released when the project started. Version 3 is also still in beta. Later, the scripts will be changed to use version 3.

- [AntWeb API version 2](https://www.antweb.org/api/v2/)
- [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

## Images / Dataset

Below you can see two images representing the dataset. One is an image of _Lasius flavus_ and the other one is a mosaic of _Tetramorium gollum_ I made using the image set.

| _Lasius flavus_ | Mosaic of _Tetramorium gollum_ |
|----------------------------------- | ----------------------------------|
|![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true) | ![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true)|

# Neural Network

## Ready to use models

- Inception v3
- Inception-ResNet V2 (recommended)
- Xception (Inception based)
- ResNet
- DenseNet (ResNet based)

## Self-made model

It is also possible to use a model made by the author by flagging the model in the configuration file as `Build`.

# Requirements

- [Python3 (3.6)](https://www.python.org/downloads/release/python-364/)
- [Keras | Why use Keras?](https://keras.io/why-use-keras/)
- [Requirements](requirements.txt)

# Credits

- Naturalis Biodiversity Center
- Supervisor: dr. Rutger Vos
- 2nd Corrector: dr. Jeremy Miller
- [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

# Why this name, FormicID?

FormicID is a concatenation of Formicidae (the family name of ants) and identification

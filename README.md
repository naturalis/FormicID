# FormicID

_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.org/naturalis/FormicID.svg?branch=master)](https://travis-ci.org/naturalis/FormicID) · 
[![Docker Build Status](https://img.shields.io/docker/build/jrottenberg/ffmpeg.svg)](https://hub.docker.com/r/marijnjaboer/formicid-auto/) · 
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · 
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · 
![Python 3.5](https://img.shields.io/badge/Python-3.6%2B-blue.svg) · 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/naturalis/FormicID/graphs/commit-activity) · 
[![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · 
[![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues) · 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


<!-- TOC depthFrom:1 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->

- [FormicID](#formicid)
- [Description](#description)
	- [Reports](#reports)
- [How to use](#how-to-use)
	- [Step 1 Get the code](#step-1-get-the-code)
	- [Step 2 Species list](#step-2-species-list)
	- [Step 3 Configuration](#step-3-configuration)
	- [Step 4 Data](#step-4-data)
	- [Step 5 Model initialisation and training](#step-5-model-initialisation-and-training)
	- [Step 6 Evaluation](#step-6-evaluation)
	- [Step 7 Optional functions](#step-7-optional-functions)
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

## Reports
### Proposal
The proposal can be found [here](https://github.com/naturalis/FormicID-proposal).

### Report
The report can be found [here](https://github.com/naturalis/FormicID-report).

# How to use
Below are some steps to get you going. Futhermore, all functions have descriptions and should get you more information.

## Step 1 Get the code
Clone the repository.

```sh
$ git clone https://github.com/naturalis/FormicID
$ cd ./FormicID
```

## Step 2 Species list

_Skip step 2 if you don't need to download the data._

Create a 2 column .csv file with the genus + species specified for downloading from AntWeb. `indet` species will be skipped because it it just a aggregation of unidentified specimens within a genus. Species that will show `0` specimen count will also be skipped.

genus  | species
------ | --------
genus1 | species1
genus2 | species2
...    | ...

### Note:
`get_species_list.py` is made to do this for you. Here you just have to set the number of minimum images you want species to have and a 2 column csv file is created with genus and species names. However, due to the problem that some species have more than 3 images (e.g. close-ups), the counting of images per species is incorrect if you just want to have dorsal, head and profile shot types. Therefore, use this script with caution.

## Step 3 Configuration
Configure the configuration file `formicID/configs/config.json` or create your own configuration file based on this one.

- Set an experiment name using `exp_name`.
- Set a data set name in `data_set`.
- Set the following (as integers):
  - `batch size` (for InceptionResNetV2: 32)
  - `dropout`
  - `learning rate`
  - `num_epochs`
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
  - `Eve` (not working as of now)
- Set the `test_split` and `val_split` as float percentages.
- Set the `shottype` to use (`dorsal`, `head`, `profile` or `stitched`).

```json
{
    "exp_name": "experiment_name",
    "data_set": "dataset_name",
    "batch_size": 32,
    "dropout": 0.5,
    "learning_rate": 0.001,
    "model": "InceptionResNetV2",
    "num_epochs": 100,
    "num_iter_per_epoch": 32,
    "optimizer": "Nadam",
    "seed": 1,
    "test_split": 0.1,
    "val_split": 0.2,
    "shottype": "head"
}
```

## Step 4 Data
Next, using the python file `get_dataset.py` you can download, stitch, split data and/or remove reproductives. 

### Downloading 
Set the correct values for the function below. This function will download json files that will hold all the information on species (such as names, catalog identifier and URLs to images). Then it will filter out the relevant information, after which it will download the images. Quality of images is one of: `low`, `medium`, `thumbview` or `high`. `Shottypes` can be `d`, `h`, or `p` or a combination of those. If you flag `multi_only` to `True`, shottypes needs to be `dhp`.

```python
get_dataset(
    input='species.csv', # The csv file from step `2.1.
    n_jsonfiles=5,       # Should be equal to the number of species from step 2
    config=config,       # The configuration file.
	shottypes="dhp",	 # Specifies the shottypes to download images
    quality='medium',    # The quality of images.
    update=True,         # Whether to update for broken URLs.
    offset_set=0,        # The offset for specimens in a JSON file.
    limit_set=99999,     # The specimen limit to add to the JSON file.
	multi_only=True		 # Flag `True` if doing multi-view
)
```

### Stitching for multi-view
Run the function below to stitch together the images from three shottypes, if you are doing the multi-view approach.

```python
stitch_maker(config=config)
```

### Splitting data
Run this function to split the data in a training, validation and test set, configured by the config file. You can also set a 1 column csv file containing bad specimens (e.g. affected by funghi, or missing bodyparts).

```python
split_in_directory(config=config, bad="data/badspecimens.csv")
```

### Removing reproductives
Together with a 1 column csv file containing catalognumbers, you can remove the reproductives from a test set using the function below.

```python
remove_reproductives(
     csv="data/reproductives.csv",
     dataset="top97species_Qmed_def_clean_wtest",
     config=config,
 )
```

## Step 5 Model initialisation and training

Now you can run `formicID/main.py` with `config.json` as a system argument and the model will be initialized, compiled and training will begin, as set by the configuration file.

### Callbacks
Possible callbacks, loaded from `utils/logger.py`, are `Tensorboard`, `EarlyStopping`, `ModelCheckpoint`, `CSVLogger` and `ReduceLROnPlateau`.

- Using TensorBoard you can get insight in training metrics.
- Earlystopping will make sure the model does not overfit and continue training for too long
- Weights will be saved every time the model is improved, based on the validation loss and at the end of training.
- A csvlogger is logging all the training and validation metrics per epoch
- Learning rate is reduced if the model has stopped improving.

## Step 6 Evaluation

After training it will be possible to launch TensorBoard to view loss, accuracy, and top-3 accuracy for training and validation. Using `evaluator()` the test set will be run against the model to see test metrics.

Further evaluation options are:
- It is possible to plot metrics, right after training, using `plot_history()`.  
- Predict labels for the test set using `predictor()`.
- Get prediction reports for the test set using `predictor_reports()` in 2 forms:
  - classification report with precision, recall, f1 and support
  - true labels and its corresponding predicted label
- Plot a confusion matrix using the species names, true labels and predicted labels using `plot_confusion_matrix()`.

### Predicting an image
Using `predict_image.py` it is possible to initialize a model, load pre-trained weights and add an image to get a classification for that image.

## Step 7 Optional functions

Utilities that can be loaded are:
- Image utilities
  - Saving data augmentation examples of 1 sample image `augmentation.py`.
  - Viewing data augmentation for 1 sample images  `show_augmentation_from_dir()`.
  - Viewing multiple images `show_multi_img()`.
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

# Project Structure

```
|-- formicID
    |-- __version__.py
	|-- augmentation.py
	|-- get_dataset.py
	|-- get_species_list.py
	|-- main.py
	|-- predict_image.py
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

Images are harvested from [www.AntWeb.org](www.antweb.org). At this moment API version 2 is used, because version 3 was still in beta when the project started. Later, the scripts could be changed to use version 3.

- [AntWeb API version 2](https://www.antweb.org/api/v2/)
- [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

## Images / Dataset

Below you can see two images representing the dataset. One is an image of _Lasius flavus_ and the other one is a mosaic of _Tetramorium gollum_ I made using the image set.

| _Lasius flavus_ | Mosaic of _Tetramorium gollum_ |
|----------------------------------- | ----------------------------------|
|![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true) | ![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true)|

# Neural Network

## Ready to use models
Inception based
- Inception v3
- Inception-ResNet V2 (recommended)
- Xception (Inception based)
ResNet based
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

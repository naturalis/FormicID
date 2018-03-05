# FormicID
_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.com/naturalis/FormicID.svg?token=1cLc3spsoyrFkzth95Ho&branch=master)](https://travis-ci.com/naturalis/FormicID) · [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](<https://GitHub.com/naturalis/FormicID/graphs/commit-activity>) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/issues/) · [![](https://img.shields.io/github/issues-closed-raw/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues?q=is%3Aissue+is%3Aclosed)

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [FormicID](#formicid)
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
You can find the proposal [here](https://github.com/naturalis/FormicID-proposal).

## :arrow_forward: How to use

### Step 1
Clone the repository
```sh
$ git clone https://github.com/naturalis/FormicID
$ cd ./FormicID
```
### Step 2
Create a 2 column csv file with the genus+species you want to download from AntWeb as follows:


| genus  | species  |
|--------|----------|
| genus1 | species1 |
| genus2 | species2 |
| genus3 | species3 |

### Step 3
Run [`formicID/main.py`](formicID/main.py) with the `urls_to_json()` function uncommented to download all the JSON objects for your species, but it will ignore `indet` species if these are in the csv file. Set the following settings in `urls_to_json`:
* `csv_file`: csvfile name
* `input_dir`: input directory
* `output_dir`: output directory
* `offset_set`: offset
* `limit_set`: limit
<!-- _(If you want all species, skip step 1 and run [`AW_to_json.py`](formicID/AntWeb/AW_to_json.py) without specifying a `genus` and `species`)_  -->
### Step 4
Run [`formicID/main.py`](formicID/main.py) with the `batch_json_to_csv()` function uncommented, so a csv file is created with the information you need to download and name images correctly to your output folder. Set the following settings in `batch_json_to_csv`):
* `input_dir`: input directory
* `output_dir`: output directory
* `csvname`: csv name for the new csv

### Step 5
In [`formicID/main.py`](formicID/main.py) the `image_scraper()` function could be uncommented to download the images. The csv file from step 3 will be updated if you flag `image_scraper(update=False/True)` as True. This will repair broken URls (usually from `blf` or `hjr` collections because AntWebs API changes `(` and `)` to `_`). After updating the csv, the script will start downloading images and will put these in newly created folders for head, dorsal and profile shots. In these folders, every species is put in its own folder. Set the following settings in `image_scraper()`:
* `csvfile`: csv file from step 3
* `input_dir`: input_dir directory of the csv file
* `start`: start number (line where to start in the csv file)
* `end`: end number (line where to end in the csv file)
* `output_dir_name`: directory name for the images
* `update`: update (whether to update the csv file for broken urls or not)


### Step 6
Configure `formicID/configs/config.json`
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

### Step 7
Run `formicID/main.py` with `config.json` as system argument and the network will train.

_To be continued_

## :bookmark: Project Structure
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
```

## :ant: AntWeb
> AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.


> Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.

_Text from Antweb.org_

### :satellite: AntWeb API
Images are harvested from [`www.AntWeb.org`](www.antweb.org). At this moment version 2 is used because version 3 was not released when the project started. Version 3 is also still in beta. Later, the scripts will be changed to use version 3.

- [AntWeb API version 2](https://www.antweb.org/api/v2/)
- [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

### :open_file_folder: Images / Dataset
Below you can see two images representing the dataset. One is an image of _Lasius flavus_ and the other one is a mosaic of _Tetramorium gollum_ I made using the image set.


| _Lasius flavus_                      | Mosaic of _Tetramorium gollum_   |
|--------------------------------------|----------------------------------|
|![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true) | ![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true)|

## :computer: Neural Network
### :mag: Ready to use models
- Inception v3 (recommended)
- Xception
- ResNet
- DenseNet

### :triangular_ruler: Self-made model
It will also be possible to use a model made by the author.

## :clipboard: Requirements
* [Keras | Why use Keras?](https://keras.io/why-use-keras/)
* [Requirements](requirements.txt)

## :scroll: Credits
- Naturalis Biodiversity Center
- Supervisor: dr. Rutger Vos
- 2nd Corrector: dr. Jeremy Miller
- [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

## :exclamation: Why this name, FormicID?
FormicID is a concatenation of Formicidae (the family name of ants) and identification

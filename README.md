# FormicID
_Classification of images of ants using deep learning_

[![Build Status](https://travis-ci.com/naturalis/FormicID.svg?token=1cLc3spsoyrFkzth95Ho&branch=master)](https://travis-ci.com/naturalis/FormicID) · [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](<https://GitHub.com/naturalis/FormicID/graphs/commit-activity>) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/issues/) · [![](https://img.shields.io/github/issues-closed-raw/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues?q=is%3Aissue+is%3Aclosed)

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [FormicID](#formicid)
	- [Description](#pencil-description)
		- [Proposal](#proposal)
	- [How to use](#arrowforward-how-to-use)
	- [Project Structure](#bookmark-project-structure)
		- [Why this name, FormicID?](#why-this-name-formicid)
	- [AntWeb](#ant-antweb)
		- [AntWeb API](#satellite-antweb-api)
		- [Images / Dataset](#openfilefolder-images-dataset)
	- [Neural Network](#computer-neural-network)
		- [Architecture](#triangularruler-architecture)
	- [Requirements](#clipboard-requirements)
	- [Credits](#scroll-credits)

<!-- /TOC -->

## :pencil: Description
Code repository for CNN-based image classification of AntWeb images<br>


![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)


_Images are harvested from AntWeb.org_

### :black_nib: Proposal
You can find the proposal [here](https://github.com/naturalis/FormicID-proposal).

## :arrow_forward: How to use
The working directory should be `/`, so pathways to `/data` work.
1. Create a 2 column csv file with the genus+species you want to download from AntWeb as follows:


| genus  | species  |
|--------|----------|
| genus1 | species1 |
| genus2 | species2 |
| genus3 | species3 |

2. Run [`AW_to_json.py`](formicID/AntWeb/AW2_to_json.py) to download all the JSON objects for your species, but it will ignore `indet` species if these are in the csv file. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/bfda5a4f03bf5b6b9e663c5f5a57b1554cedd8f1/formicID/AntWeb/AW2_to_json.py#L159):
    * `csv_file`: csvfile name
    * `input_dir`: input directory
    * `output_dir`: output directory
    * `offset_set`: offset
    * `limit_set`: limit
<!-- _(If you want all species, skip step 1 and run [`AW_to_json.py`](formicID/AntWeb/AW_to_json.py) without specifying a `genus` and `species`)_  -->
3. Run [`json_to_csv.py`](formicID/AntWeb/json_to_csv.py) so a csv file is created with the information you need to download and name images correctly to your output folder. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/bfda5a4f03bf5b6b9e663c5f5a57b1554cedd8f1/formicID/AntWeb/json_to_csv.py#L115):
    * `input_dir`: input directory
    * `output_dir`: output directory
    * `csvname`: csv name for the new csv
4. Using [`scrape.py`](formicID/data_scraper/scrape.py) the csv file from step 3 will be updated if you flag `image_scraper(update=False/True)` as True. This will repair broken URls (usually from `blf` or `hjr` collections because AntWebs API changes `(` and `)` to `_`). After updating the csv, the script will start downloading images and will put these in newly created folders for head, dorsal and profile shots. In these folders, every species is put in its own folder. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/bfda5a4f03bf5b6b9e663c5f5a57b1554cedd8f1/formicID/data_scraper/scrape.py#L207):
    * `csvfile`: csv file from step 3
    * `input_dir`: input_dir directory of the csv file
    * `start`: start number (line where to start in the csv file)
    * `end`: end number (line where to end in the csv file)
    * `output_dir_name`: directory name for the images
    * `update`: update (whether to update the csv file for broken urls or not)

_To be continued_

## :bookmark: Project Structure
```
|-- FormicID
    |-- __init__.py
    |-- AntWeb
    |   |-- AW_to_json.py
    |   |-- __init__.py
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
    |   |-- main.py
    |-- models
    |   |-- __init__.py
    |   |-- build.py
    |   |-- models.py
    |-- testers
    |   |-- __init__.py
    |   |-- formicID_test.py
    |-- trainers
    |   |-- __init__.py
    |   |-- train.py
    |-- utils
        |-- __init__.py
        |-- utils.py
```
### :exclamation: Why this name, FormicID?
FormicID is a concatenation of Formicidae (the family name of ants) and identification

## :ant: AntWeb
> AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.<br><br>
Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.<br><br>
_Text from Antweb.org_<br><br>
![](https://github.com/naturalis/FormicID/blob/master/img/lasiusflavus.jpg?raw=true)<br>

### :satellite: AntWeb API
- [AntWeb API version 2](https://www.antweb.org/api/v2/)
- [AntWeb API version 3 beta](https://www.antweb.org/documentation/api/apiV3.jsp)

At this moment version 2 is used because version 3 was not released when the project started. Version 3 is also still in beta. Later, the scripts will be changed to use version 3.

### :open_file_folder: Images / Dataset
How does the dataset looks like<br><br>
![](https://github.com/naturalis/FormicID/blob/master/img/mosaic.jpg?raw=true)<br>

## :computer: Neural Network
### :triangular_ruler: Architecture
Text on how the neural network architecture looks like

## :clipboard: Requirements
* [Keras | Why use Keras?](https://keras.io/why-use-keras/)
* [Requirements](requirements.txt)

## :scroll: Credits
- Naturalis Biodiversity Center
- Supervisor: dr. Rutger Vos
- 2nd Corrector: dr. Jeremy Miller
- [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

# FormicID

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![GitHub followers](https://img.shields.io/github/followers/MarijnJABoer.svg)](https://github.com/MarijnJABoer?tab=followers) · [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](www.marijnboer.nl) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](<https://GitHub.com/naturalis/FormicID/graphs/commit-activity>) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/issues/) · [![](https://img.shields.io/github/issues-closed-raw/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues?q=is%3Aissue+is%3Aclosed)

_Classification of images of ants using deep learning_

<details>
  <summary>Table of content (click to open) </summary>
  <p>
</p>
  <ul>
  <li><a href="#description">Description</a></li>
  <li><a href="#quickstart">Quickstart</a></li>
  <li><a href="#antweb">AntWeb</a><ul><li><a href="#antweb-api">AntWeb API</a></li><li><a href="#images--dataset">Dataset</a></li></ul></li>
  <li><a href="#neural-network">Neural Network</a><ul><li><a href="#architecture">Architecture</a></li></ul></li>
  <li><a href="#requirements">Requirements</a></li>
  <li><a href="#credits">Credits</a></li>
</ul>
</details>

--------------------------------------------------------------------------------
## :pencil: Description

Code repository for CNN-based image classification of AntWeb images<br>
_FormicID is Formicidae / IDentification_<br>
![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)<br>
_Images are taken from AntWeb.org_

## :arrow_forward: How to use

1. Create a 2 column csv file with the genus+species you want to download from AntWeb.
2. Run [`AW_to_json.py`](AW_to_json.py) to download all the JSON objects for your species.
(If you want all species, skip step 1 and run [`AW_to_json.py`](AW_to_json.py) without specifying a `genus` and `species`)
3. run [`json_to_csv.py`](json_to_csv.py) so a csv file is created with the information you need to download and name images correctly to your output folder.
4. _To be continuted_

## :bookmark: Project Structure
`
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

`

## :ant: AntWeb

AntWeb is the world's largest online database of images, specimen records, and natural history information on ants. It is community driven and open to contribution from anyone with specimen records, natural history comments, or images.<br><br>
Our mission is to publish for the scientific community high quality images of all the world's ant species. AntWeb provides tools for submitting images, specimen records, annotating species pages, and managing regional species lists.<br><br>
_Text taken from Antweb.org_<br><br>
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

[Requirements](requirements.txt)

## :scroll: Credits

- Naturalis Biodiversity Center
- Supervisor: dr. Rutger Vos
- 2nd Corrector: dr. Jeremy Miller
- [Bookmarks and Resources](docs/Bookmarks-and-resources.md)

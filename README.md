# FormicID

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/naturalis/FormicID/blob/master/LICENSE) · [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) · [![GitHub followers](https://img.shields.io/github/followers/MarijnJABoer.svg)](https://github.com/MarijnJABoer?tab=followers) · [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](<www.marijnboer.nl>) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](<https://GitHub.com/naturalis/FormicID/graphs/commit-activity>) · [![GitHub contributors](https://img.shields.io/github/contributors/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/graphs/contributors/) · [![GitHub issues](https://img.shields.io/github/issues/naturalis/FormicID.svg)](https://GitHub.com/naturalis/FormicID/issues/) · [![](https://img.shields.io/github/issues-closed-raw/naturalis/FormicID.svg)](https://github.com/naturalis/FormicID/issues?q=is%3Aissue+is%3Aclosed)

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
<br>
![](https://github.com/naturalis/FormicID/blob/master/img/25images.gif?raw=true)<br>
_Images are harvested from AntWeb.org_



## :arrow_forward: How to use
The working directory should be `/`, so pathways to `/data` work.
1. Create a 2 column csv file with the genus+species you want to download from AntWeb as follows:


| genus  | species  |
|--------|----------|
| genus1 | species1 |
| genus2 | species2 |
| genus3 | species3 |

2. Run [`AW_to_json.py`](formicID/AntWeb/AW_to_json.py) to download all the JSON objects for your species, but it will ignore `indet` species if these are in the csv file. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/87ebd643f880c13bba48f2ce7a1405a151704052/formicID/AntWeb/AW_to_json.py#L174):
    * csvfile name
    * input directory
    * output directory
    * offset
    * limit
<!-- _(If you want all species, skip step 1 and run [`AW_to_json.py`](formicID/AntWeb/AW_to_json.py) without specifying a `genus` and `species`)_  -->
3. Run [`json_to_csv.py`](formicID/AntWeb/json_to_csv.py) so a csv file is created with the information you need to download and name images correctly to your output folder. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/87ebd643f880c13bba48f2ce7a1405a151704052/formicID/AntWeb/json_to_csv.py#L115):
    * input directory
    * output directory
    * csv name for the new csv
4. Using [`scrape.py`](formicID/data_scraper/scrape.py) the csv file from step 3 will be updated if you flag `image_scraper(update=False/True)` as True. This will repair broken URls (usually from `blf` or `hjr` collections because AntWebs API changes `(` and `)` to `_`). After updating the csv, the script will start downloading images and will put these in newly created folders for head, dorsal and profile shots. In these folders, every species is put in its own folder. Set the following settings in [`main()`](https://github.com/naturalis/FormicID/blob/87ebd643f880c13bba48f2ce7a1405a151704052/formicID/data_scraper/scrape.py#L207):
    * csv file from step 3
    * input_dir directory of the csv file
    * start number (line where to start in the csv file)
    * end number (line where to end in the csv file)
    * directory name for the images
    * update (whether to update the csv file for broken urls or not)

_To be continuted_

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
### Why this name, FormicID?
FormicID is a concatenation of Formicidae (the family name of ants) and identification

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

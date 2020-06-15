# BioTaxGeo

BioTaxGeo is a web-based application to assess the geospatial and taxonomic quality of primary biodiversity data, and helps to identify and correct errors in the field collection worksheets (.xls or .csv). With a light and intuitive web interface, BioTaxGeo aims to provide good user experiences to biologists and researchers who seek the quality of biodiversity data.

<p align="center"><img src="files/images/index.jpeg" width="740" height="460"></p>

## Sumary
   - [Functionalities](#functionalities)
      - [Taxonomy Check](#taxonomy-check)
      - [Occurrence Check](#occurrence-check)
      - [Comparison between Spreadsheets](#comparison-between-spreadsheets)
   - [Installation Guide](#installation-Guide)
   - [Authors](#authors)
   - [License](#license)
   
## Functionalities


<p align="center"><img src="files/images/ScreenshotIndex.png" width="740" height="460"></p>



### Taxonomy Check

The user will submit a spreadsheet to check the taxonomy fields of all records of the species collected. BioTaxGeo will check if the taxonomy is valid, if there are problems in the taxonomic data the system will suggest corrections according to the screens below. The taxonomic checking process is done via Species API in Global Biodiversity Information Facility ( <a href="https://www.gbif.org/" target="_blank">GBIF</a> ) database. 

<p align="center"><img src="files/images/pt1.gif" width="740" height="460"></p>

> In this screen, the user must correctly select the fields referring to the taxonomy present in his spreadsheet, so that the application can validate it.

<p align="center"><img src="files/images/pt2.gif" width="740" height="460"></p>

> Then the taxonomic data of the spreadsheet will be checked. If there is any problem in filling it out, the application will point out the flaws and suggest corrections. The user can save the changes in the spreadsheet itself, if desired.

<p align="center"><img src="files/images/pt3&#32;2.gif" width="740" height="460"></p>

### Occurrence Check

The user will inform the longitude and latitude fields present in the spreadsheet and must also inform the location of the species collection site, inserting markers on a map that will delimit the area forming a polygon. BioTaxGeo will check if there are inconsistencies in the data of the filled geographic coordinates, or if the data of the coordinates of the collected species are within the mapped area. The coordinate verification process is done via Google's Geocoding API.

> The first step is to select the correct card.

<p align="center"><img src="files/images/map-pt1.gif" width="740" height="460"></p>

> Select the corresponding columns in your spreadsheet file.

<p align="center"><img src="files/images/map-pt2.gif" width="740" height="460"></p>

> Then you will be redirected to plot markers and identify the area you collected the data. The user will be able to inform the geographical coordinates of the plot markers by clicking directly on the map or entering data in the longitude and latitude fields

<p align="center"><img src="files/images/map-pt3.gif" width="740" height="460"></p>

> Together with a list containing suggestions for possible incorrect entries.

> Validations will be availible at this point for modify the data in your spreadsheet file and save changes if you like.

<p align="center"><img src="files/images/map-pt4.gif" width="740" height="460"></p>

### Comparison between Spreadsheets

This section will ask for you to fill the fields correctly to identify the columns for `two` spreadsheet files.

> Insert the file that will be used as reference.

<p align="center"><img src="files/images/localsheet-pt1.gif" width="740" height="460"></p>

> Identify the columns in both files.

<p align="center"><img src="files/images/localsheet-pt2.gif" width="740" height="460"></p>

> After the software identify your columns, the data will be compared the entries between them.

<p align="center"><img src="files/images/localsheet-pt3.gif" width="740" height="460"></p>

## Installation Guide

### Requirement
- API KEY GoogleMaps
- python ^3.6
- virtualenv

### API GoogleMaps
How to get API: https://developers.google.com/maps/documentation/javascript/get-api-key

Active API for Geocoding API  and Maps JavaScript API.

At the root of the project open the file googlemaps_api_key.txt, paste your API KEY save and close the file.
### Virtualenv
How to install and run virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

How to use : https://virtualenv.pypa.io/en/latest/user_guide.html

### Step 1: Download project
Download the project or clone it into a folder on your PC.
### Step 2: Init virtualenv
Inside the folder create a virtualenv with a version of Python 3.6^. Open the terminal (if you are using Windows you will need to use the terminal as an administrator), start your virtualenv.
### Step 3: Install packages
Use this command to install:
> pip install (package name)==(version number)

Install the packages below.

- flask (version 1.1.1)
- fuzzywuzzy (version 0.18.0)
- python-Levenshtein-wheels (version 0.13.1)
- requests (version 2.23.0)
- xlrd (version 1.2.0)
- xlutils (version 2.0.0)
- xlwt (version 1.3.0)
- googlemaps (version 4.2.0)
- pandas (version 1.0.4)
### Step 4: Starting the software
Now execute the code:

> python run.py

The server will be started at http: // localhost: 8080.

Make sure that you are using virtualenv and that all packages are installed correctly, also make sure you paste the google maps API code into googlemaps_api_key.txt file before running the program.
### Authors

- Marcos Paulo Alves de Sousa (Project leader)
  - email: marcosp.belem@gmail.com
  - github: <a href="https://github.com/marcosp-sousa" target="_blank">marcosp-sousa</a>
- Elielson Fernando dos Santos Barbosa
  - email: elielsonbr.com@gmail.com
  - github: <a href="https://github.com/Elielson68" target="_blank">Elielson68</a>
- Renan Figueiredo Carneiro
  - email: renanfigcarneiro@gmail.com
  - github: <a href="https://github.com/rnanc" target="_blank">rnanc</a>

### License

- MIT License. See [LICENSE](https://github.com/marcosp-sousa/BioTaxGeo/blob/master/LICENSE) for more information

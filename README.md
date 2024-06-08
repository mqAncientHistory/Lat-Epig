# Welcome to the Latin Epigraphy Scraper (*LatEpig*) v2.0

![Project_status](https://img.shields.io/badge/status-finalised%20development-brightgreen%20%22Project%20status%20logo%22 "Project status logo")
![Version](https://img.shields.io/badge/version-2.0-blue "Version")

*The **LatEpig** tool allows you to query all the inscriptions from the Epigraphic Database Clauss Slaby (www.manfredclauss.de) in a reproducible manner: it saves the search results in a TSV and a JSON file and plots them on an interactive map of the Roman Empire without any prior knowledge of programming in a matter of minutes.*

<p align="center">
  <img src="https://github.com/mqAncientHistory/Lat-Epig/blob/main/images/2022-10-20-EDCS_via_Lat_Epig-term1_viator-692-Provinces_in_AD_117-Citiesall-Roadsall-multicolour-DPI600-.png" width="100%" alt="Lat Epig map showing inscriptions containing the term viator (a passer-by), Petra Hermankova, 20/10/2022, epigraphic data: Epigraphic Database Clauss-Slaby" style="border:1px solid black"/>
</p>

---

## Authors 
* Brian Ballsun-Stanton, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-4932-7912)
* Petra Heřmánková, Aarhus University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540)
* Ray Laurence, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-8229-1053)

## Description 

This program allows to extraction of the output of a search query from the [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) in a reproducible manner and saves it as a TSV file (i.e. *tab separated value*) that can be easily opened in your favourite spreadsheet software, or as a JSON file. The search results can be also plotted to a map of the Roman Empire, along with the system of the Roman Provinces, roads, and cities. More on the used datasets in the `Data Sources` section.


## Cite this software

**Ballsun-Stanton B., Heřmánková P., Laurence R. *LatEpig* (version 2.0). GitHub. URL: <https://github.com/mqAncientHistory/Lat-Epig/> DOI: [10.5281/zenodo.5211341](https://doi.org/10.5281/zenodo.5211341)**

If you're using this tool in your research, <!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/mqAncientHistory/Lat-Epig" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" data-show-count="true" aria-label="Star mqAncientHistory/Lat-Epig on GitHub">Star</a> us on Github! (This way, we don't need to put tracking pixels into this notebook to get a sense of how many folks are using our tool!) 

If you find a bug or have a feature request, raise an <!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/mqAncientHistory/Lat-Epig/issues" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-issue-opened" data-show-count="true" aria-label="Issue mqAncientHistory/Lat-Epig on GitHub">Issue</a>!


---

## 1. How to run *LatEpig* with a single click (using online Jupyter Notebooks on myBinder)

*To launch Lat-Epig on myBinder click on the following icon* 
[![*LatEpig* on myBinder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/Lat-Epig/HEAD?urlpath=notebooks/EpigraphyScraper.ipynb)

No need for powerful computer, as the tool runs on external servers with a single click. This option is ideal if you want to test the tool or do small searches (with up to 1000 results). Searches with more than 1000+ results will still run, however, the interactive map may not be created or it may take a long time as the memory on the myBinder is limited. For creation of interactive maps based on large searches, we recommend using the Docker option (see below).

When the Jupyter Notebook starts, click the fast-forward button, or choose the `Kernel menu` from the top bar and choose `Restart & Run All`. Further step-by-step instructions and search examples are provided within the Jupyter Notebook.


## 2. How to run *LatEpig* on your computer using Docker

1. Install Docker on your computer. See instructions for your OS ([Windows instructions](https://hub.docker.com/editions/community/docker-ce-desktop-windows), [Linux instructions](https://docs.docker.com/engine/install/ubuntu/) + [Add users to Docker inscructions](https://docs.docker.com/engine/install/linux-postinstall/), [Mac instructions](https://docs.docker.com/docker-for-mac/install/))
1. Start Docker
1. Open a Command Line / Terminal
1. Test if Docker runs by running
`docker run hello-world`
1. If you see the following message, you have installed Docker successfully:
`Hello from Docker! This message shows that your installation appears to be working correctly.`
1. Now run the following to start the *LatEpig* within Docker. You will need a stable internet connection as you will download almost 2 GB.
`docker run -p 8888:8888 denubis/lat-epig-scraper:main`
1. Go to your browser (Firefox, Chrome...) and paste in 
`http://localhost:8888/notebooks/EpigraphyScraper.ipynb` and you should see the *LatEpig* interface.

*Note: If your computer is low on memory, we recommend using Firefox instead of Chrome. If you have troubles starting Docker, close Chrome, and all non-essential software and try again with Firefox browser.*

## 3. For Developers (local build):

_For testing or development purposes mainly. We recommend using Ubuntu 22.04+._

**Run the following code inside a virtualised environment using direnv and pyenv**
```
sudo apt-get update && sudo apt-get install -y --no-install-recommends apt-transport-https apt-utils build-essential ca-certificates curl git libbz2-dev libffi-dev libgeos++-dev liblzma-dev libncurses5-dev libproj-dev libreadline-dev libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev make proj-bin proj-data python3-pip wget zlib1g-dev libgeos-dev libxml2-dev libxslt-dev python-dev libc6 libgcc-s1 libgeos-c1v5 libproj15 libstdc++6 libpython3.8-dev python3.8 python3.8-tk
curl -fsSL https://deb.nodesource.com/setup_15.x | bash -
sudo apt-get install -y --no-install-recommends  nodejs
pip3 install numpy==1.20.1 cython wheel
pip3 install --no-cache-dir -r requirements.txt 
jupyter nbextension enable --py widgetsnbextension --sys-prefix &&  jupyter labextension install @jupyter-widgets/jupyterlab-manager &&   jupyter labextension install @voila-dashboards/jupyterlab-preview &&  jupyter serverextension enable voila --sys-prefix &&  jupyter contrib nbextension install --sys-prefix &&   jupyter nbextension enable init_cell/main
jupyter trust EpigraphyScraper.ipynb 
jupyter lab EpigraphyScraper.ipynb 
```
Next, rerun all cells of the Jupyter Notebook.

_Optional_
Running `voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb ` may provide a cleaner UI than Jupyter Notebook.


---


## Data Sources
### Inscriptions

The [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) is a digital collection of more than 500,000 Latin inscriptions, created by Prof. Manfred Clauss, Anne Kolb, Wolfgang A. Slaby, Barbara Woitas, and hosted by the Universitat Zurich and Katolische Universitat Eichstat-Ingoldstadt.

### Interactive Map

#### Roman Empire Boundaries & Provinces

[Ancient World Mapping Centre, political shading shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/cultural_data/political_shading/), following the Barrington Atlas of Greek-Roman World, [AWMC.UNC.EDU ], under the Creative Commons Attribution-NonCommercial 4.0 International License. 

1. Roman Empire 60 BC (provinces or extent)
1. Roman Empire in AD 14 (provinces or extent)
1. Roman Empire in AD 69 (provinces or extent)
1. Roman Empire in AD 117 (DEFAULT, provinces or extent)
1. Roman Empire in AD 200 (provinces or extent)

#### Roman Roads

1. McCormick, M. et al. 2013. *Roman Road Network (version 2008)*, DARMC Scholarly Data Series, Data Contribution Series #2013-5. DARMC, Center for Geographic Analysis, Harvard University, Cambridge MA 02138.

1. [Ancient World Mapping Centre, road shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/ba_roads/), shapefile for roads, following the Barrington Atlas of Greek-Roman World, under the Creative Commons Attribution-NonCommercial 4.0 International License. Collection of shapefiles also vailable through the [UCD Digital Library](https://digital.ucd.ie/view/ucdlib:23000)

#### Cities

1. The shapefile of the cities used in the map is based on Hanson, J. W. (2016). *Cities Database (OXREP databases)*. Version 1.0. Accessed (date): <http://oxrep.classics.ox.ac.uk/databases/cities/>. DOI: <https://doi.org/10.5287/bodleian:eqapevAn8>. More info is available through Hanson, J. W. (2016b). *An Urban Geography of the Roman World, 100 B.C. to A.D. 300.* Oxford: Archaeopress.

---

### Metadata for the files produced by *LatEpig*

Each TSV and JSON file contains the information from EDCS separated into 22 attributes. The [*LatEpig* Metadata description](https://github.com/mqAncientHistory/Lat-Epig/blob/main/LatEpig_Metadata_Description.txt) document in the GitHub repo describes the contents of individual attributes along with their description and their original source. 

Note that the *file name* in both formats contains the date of your search, the source of the data and how it was accessed (EDCS via *LatEpig*) and any search parameters or their combinations you have used (*Term 1, Term 2, Dating from*...) and the number of inscriptions found. This way you will always remember what you have searched for and when you share the file with a colleague or students, they can always replicate your search to see if any new inscriptions were added to EDCS. The same applies to the publication quality maps (experimental feature) produced by *LatEpig*: they all contain the search parameters by default, alongside the origin of information and credit - all in the spirit of the best research practice and FAIR data principles.

### Generation of new attributes

#### Customised cleaning of the epigraphic text and unit testing [#unittests]

The text of the inscription is available in three different formats as three separate attributes: 
1. ‘inscription’ - the original text as presented by EDCS with all original markup and symbols, including the Leiden Conventions  markup for editions of inscriptions; 
2. ‘inscription_conservative_cleaning’ - the result of the custom cleaning function embedded in the Lat/Epig software, producing a conservative version of the text of an inscription. The text is as close to the preserved state of the text, without restorations and expansions also known as the diplomatic edition (only the characters as they appear on the support, with minimal or no editorial intervention or interpretation)
3. ‘inscription_interpretive_cleaning’ - the result of the custom cleaning function embedded in the Lat/Epig software, producing an interpretative version of the text of an inscription. The text contains all restorations and expansions to obtain as rich a version of the text as possible, interpunction between sentences is not preserved. This text version is most suitable for quantitative text analysis methods and NLP.

For details, see the structure of [both cleaning functions](https://github.com/mqAncientHistory/Lat-Epig/blob/main/src/lat_epig/text_parse.py) and [their unit tests](https://github.com/mqAncientHistory/Lat-Epig/blob/main/src/lat_epig/test_inscriptions.py).

**Unit tests** for selected attributes, and overall functionality: [dates](https://github.com/mqAncientHistory/Lat-Epig/blob/main/src/lat_epig/test_dates.py), [language](https://github.com/mqAncientHistory/Lat-Epig/blob/main/src/lat_epig/test_language.py),[, [data access](https://github.com/mqAncientHistory/Lat-Epig/blob/main/src/lat_epig/test_scrape.py). 


For feedback, or to report bugs, please use the [Github Issues](https://github.com/mqAncientHistory/Lat-Epig/issues).



**Happy epigraphic explorations!**

---




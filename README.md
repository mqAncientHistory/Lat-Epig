# Lat Epig 2.0

*The Lat-Epig inteface allows you to query the EDCS and save the search result in a TSV (tab separated value) file and plot the results on a map of the Roman Empire without any prior knowledge of programming.*

<p align="center">
  <img src="https://github.com/mqAncientHistory/Lat-Epig/blob/main/images/2021-08-16-term1_viator-690-Provinces_in_AD_117-Citiesall-Roadsall-multicolour-DPI600-.png" width="100%" alt="Lat Epig map showing inscriptions containing the term viator (a passer-by), Petra Hermankova, 16/08/2021, epigraphic data: Epigraphic Database Clauss-Slaby" style="border:1px solid black"/>
</p>

---

## Authors 
* Brian Ballsun-Stanton, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-4932-7912)
* Petra Heřmánková, Aarhus University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540)
* Ray Laurence, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-8229-1053)

## Description 

This programme extracts the output of a search query from the [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) in a reproducible manner and saves it as a TSV file. The output can be also plotted to a map of the Roman Empire, along with the system of Roman Provinces, roads, and cities. More on used datasets in the `Data Sources` section.

## Cite this software

Ballsun-Stanton B., Heřmánková P., Laurence R. *Lat Epig* (version 2.0). GitHub. URL: <https://github.com/mqAncientHistory/Lat-Epig/> DOI: [10.5281/zenodo.5211341](https://doi.org/10.5281/zenodo.5211341)

## Run Lat Epig with a single click

*To launch Lat-Epig on myBinder (as Voila application) click on the following icon* 
[![LatEpig on myBinder (VOILA)](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/Lat-Epig/HEAD?urlpath=voila/render/EpigraphyScraper.ipynb)

No need for powerful computer, as the tool runs on external servers with a single click. This option is ideal if you want to test the tool or do small searches (with up to 1000 results). Searches with more than 1000+ results will still run, however, the interactive map may not be created. For creation of interactive maps based on large searches we recommend to use some of the other options (see below).

---

## Data Sources
### Inscriptions

The [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) is a digital collection of more than 500,000 Latin inscriptions, created by Prof. Manfred Clauss, Anne Kolb, Wolfgang A. Slaby, Barbara Woitas, and hosted by the Universitat Zurich and Katolische Universitat Eichstat-Ingoldstadt.

### Map

#### Roman Empire Boundaries & Provinces

[Ancient World Mapping Centre, political shading shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/cultural_data/political_shading/), following the Barington Atlas of Greek Roman World, [AWMC.UNC.EDU ], under the Creative Commons Attribution-NonCommercial 4.0 International License. 

1. Roman Empire 60 BC (provinces or extent)
1. Roman Empire in AD 14 (provinces or extent)
1. Roman Empire in AD 69 (provinces or extent)
1. Roman Empire in AD 117 (DEFAULT, provinces or extent)
1. Roman Empire in AD 200 (provinces or extent)

#### Roman Roads

1. McCormick, M. et al. 2013. "Roman Road Network (version 2008)," DARMC Scholarly Data Series, Data Contribution Series #2013-5. DARMC, Center for Geographic Analysis, Harvard University, Cambridge MA 02138.

1. [Ancient World Mapping Centre, road shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/ba_roads/), shapefile for roads, following the Barington Atlas of Greek Roman World, under the Creative Commons Attribution-NonCommercial 4.0 International License. Collection of shapefiles also vailable through the [UCD Digital Library](https://digital.ucd.ie/view/ucdlib:23000)

#### Cities

1. The shapefile of the cities used in the map is based on Hanson, J. W. (2016). Cities Database (OXREP databases). Version 1.0. Accessed (date): <http://oxrep.classics.ox.ac.uk/databases/cities/>. DOI: <https://doi.org/10.5287/bodleian:eqapevAn8>. 

1. Hanson, J. W. (2016b). An Urban Geography of the Roman World, 100 B.C. to A.D. 300. Oxford: Archaeopress.

---

## Other options how to run *Lat Epig*

### 1. To run as Jupyter Notebook on myBinder:

Click here: [![Lat Epig on myBinder (Jupyter)](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/Lat-Epig/HEAD?urlpath=notebooks/EpigraphyScraper.ipynb)

When it starts, click the fast-forward button, or choose the Kernel menu and choose `Restart & Run All`.

_This option should be used for testing, smaller searches, or demonstration of the Lat Epig. Large searches may take long and may not render properly (as the memory on the myBinder is limited). If you need to perform large seraches, we recommend using the Docker option._

### 2. To run on your computer as Voila in Docker:

1. Install docker on your computer.
 - [Windows instructions](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
 - [Linux instructions](https://docs.docker.com/engine/install/ubuntu/) + [Add users to Docker inscructions](https://docs.docker.com/engine/install/linux-postinstall/)
 - [Mac instructions](https://docs.docker.com/docker-for-mac/install/)
1. Start Docker
1. Open a Command Line / Terminal
1. Test if Docker runs by running
`docker run hello-world`
1. If you see the following message, you have installed Docker succesfully:
`Hello from Docker! This message shows that your installation appears to be working correctly.`
1. Now run the following to start the Lat Epig within Docker. You will need a stable internet connection.
`docker run -p 8888:8888 denubis/lat-epig-scraper:main`
1. Go to your browser (Firefox, Chrome...) and paste in 
`http://localhost:8888/voila/render/EpigraphyScraper.ipynb` and you should see the Lat Epig interface.

*Note: If your computer is low on memory, we recommend using Firefox instead of Chrome. If you have troubles starting Docker, close Chrome, and all non-essential software and try again with Firefox browser.*

### 3. For Developers (local build):

_We recommend using Ubuntu 18.04+. For testing or development purposes mainly._

**Run the following code inside a virtualised environment using direnv and pyenv**
```
sudo apt-get update && sudo apt-get install -y --no-install-recommends apt-transport-https apt-utils build-essential ca-certificates curl git libbz2-dev libffi-dev libgeos++-dev liblzma-dev libncurses5-dev libproj-dev libreadline-dev libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev make proj-bin proj-data python3-pip wget zlib1g-dev libgeos-dev libxml2-dev libxslt-dev python-dev libc6 libgcc-s1 libgeos-c1v5 libproj15 libstdc++6 libpython3.8-dev python3.8 python3.8-tk
curl -fsSL https://deb.nodesource.com/setup_15.x | bash -
sudo apt-get install -y --no-install-recommends  nodejs
pip3 install numpy==1.20.1 cython wheel
pip3 install --no-cache-dir -r requirements.txt 
jupyter nbextension enable --py widgetsnbextension --sys-prefix && 	jupyter labextension install @jupyter-widgets/jupyterlab-manager && 	jupyter labextension install @voila-dashboards/jupyterlab-preview && 	jupyter serverextension enable voila --sys-prefix && 	jupyter contrib nbextension install --sys-prefix && 	jupyter nbextension enable init_cell/main
jupyter trust EpigraphyScraper.ipynb 
jupyter lab EpigraphyScraper.ipynb 
```
Next, rerun all cells of the Jupyter Notebook.

_Optional_
Running `voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb ` may provide a cleaner UI than Jupyter Notebook.


For feedback, or to report bugs, please use the [Github Issues](https://github.com/mqAncientHistory/Lat-Epig/issues).

# Lat Epig 2.0


*The Jupyter Notebook inteface allows you to query the EDCS and save the search result in a CSV file and plot the results on a map of the Roman Empire without any prior knowledge of programming.*

## Authors 
* Brian Ballsun-Stanton, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-4932-7912)
* Petra Heřmánková, Aarhus University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540)
* Ray Laurence, Macquarie University, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-8229-1053)

## Description 

This  programe extracts the output of a search query from the [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) in a reproducible manner and saves it as a CSV file. The output can be also plotted the output to a map of the Roman Empire, along with the system of Roman Provinces, roads, and cities. 

# Launch this on myBinder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/EpigraphyScraperNotebook/HEAD?urlpath=voila/render/EpigraphyScraper.ipynb)




## Data Sources
### Inscriptions

The [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) is a digital collection of more than 500,000 Latin inscriptions, created by Prof. Manfred Clauss, Anne Kolb, Wolfgang A. Slaby, Barbara Woitas, and hosted by the Universitat Zurich and Katolische Universitat Eichstat-Ingoldstadt.

### Map

#### Roman Empire Boundaries & Provinces

[Ancient World Mapping Centre, political shading shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/cultural_data/political_shading/), following the Barington Atlas of Greek Roman World, [AWMC.UNC.EDU ], under the Creative Commons Attribution-NonCommercial 4.0 International License. 

1. Roman Empire 60 BC
1. Roman Empire in AD 14
1. Roman Empire in AD 117
1. Roman Empire in AD 200

#### Roman Roads

1. McCormick, M. et al. 2013. "Roman Road Network (version 2008)," DARMC Scholarly Data Series, Data Contribution Series #2013-5. DARMC, Center for Geographic Analysis, Harvard University, Cambridge MA 02138.

1. [Ancient World Mapping Centre, road shapefiles](http://awmc.unc.edu/awmc/map_data/shapefiles/ba_roads/), shapefile for roads, following the Barington Atlas of Greek Roman World, under the Creative Commons Attribution-NonCommercial 4.0 International License. Collection of shapefiles also vailable through the [UCD Digital Library](https://digital.ucd.ie/view/ucdlib:23000)

#### Cities

1. The shapefile of the cities used in the map is based on Hanson, J. W. (2016). Cities Database (OXREP databases). Version 1.0. Accessed (date): <http://oxrep.classics.ox.ac.uk/databases/cities/>. DOI: <https://doi.org/10.5287/bodleian:eqapevAn8>. 

1. Hanson, J. W. (2016b). An Urban Geography of the Roman World, 100 B.C. to A.D. 300. Oxford: Archaeopress.


---

## Instructions how to use the tool

### To run the notebook on myBinder:

Click here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/EpigraphyScraperNotebook/HEAD?urlpath=notebooks/EpigraphyScraper.ipynb)

When it starts, click the fast-forward button, or choose the Kernel menu and choose `Restart & Run All`


### To run locally using the latest image:

`docker run -p 8888:8888 denubis/lat-epig-scraper:main` then visit <http://localhost:8888/voila/render/EpigraphyScraper.ipynb> in your browser.

### To test docker locally:

`docker build https://github.com/mqAncientHistory/EpigraphyScraperNotebook.git -t epigraphyscraper && docker run -it -p 8866:8888 epigraphyscraper`

`http://127.0.0.1:8866/notebooks/EpigraphyScraper.ipynb`

### To build locally:

**Do this inside a virtualised environment using direnv and pyenv**

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

Then rerun all cells of the Notebook.

Running `voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb ` may provide a cleaner UI than Jupyter Lab, if it works.


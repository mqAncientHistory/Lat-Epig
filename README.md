# EpigraphyScraperNotebook

To run the notebook on mybinder:

Click here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/EpigraphyScraperNotebook/HEAD?filepath=EpigraphyScraper.ipynb)

When it starts, click the fast-forward button, or choose the Kernel menu and choose "Restart & Run All"


** MAKE SURE TO RUN THIS IN A VIRUTAL ENVIRONMENT**

Deploy [direnv](https://direnv.net/docs/installation.html) and [pyenv](https://github.com/direnv/direnv/wiki/Python#pyenv). 

Run in your terminal:
```
sudo apt build-dep python3-mechanicalsoup python3-bs4  python3-tk python3-lxml python3-clint python3-rtree python3-geopandas  python3-numpy python3-pandas python3-geopy python3-shapely python3-cartopy

pip3 install numpy cython
pip3 install -r requirements.txt
jupyter notebook 'Epigraphy Scraper.ipynb'
``` 

# epigraphy-maps-from-scraper

```
pip install --upgrade pip wheel
wget http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/proj-data_7.2.0-1_all.deb http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/libproj19_7.2.0-1_amd64.deb http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/proj-bin_7.2.0-1_amd64.deb
sudo apt install $HOME/Downloads/*proj*.deb
sudo apt install libgeos-dev libproj-dev libgdal-dev
sudo apt build-dep python-geopandas scipy
pip install --force-reinstall --ignore-installed --no-binary shapely pygeos -r requirements.txt 
```

 to make sure all system gdal, etc libraries are up to date.

 Rebuilding all is unfortunately necessary because of system projection funtimes.


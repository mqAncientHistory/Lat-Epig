# EpigraphyScraperNotebook

Load into Jupyter Notebook
pip3 install -r requirements.txt

# epigraphy-maps-from-scraper


** MAKE SURE TO RUN THIS IN A VIRUTAL ENVIRONMENT**

Deploy [direnv](https://direnv.net/docs/installation.html) and [pyenv](https://github.com/direnv/direnv/wiki/Python#pyenv). 

```
$ pip install --upgrade pip wheel
$ wget http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/proj-data_7.2.0-1_all.deb http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/libproj19_7.2.0-1_amd64.deb http://mirrors.kernel.org/ubuntu/pool/universe/p/proj/proj-bin_7.2.0-1_amd64.deb
$ sudo apt install $HOME/Downloads/*proj*.deb
$ sudo apt install libgeos-dev libproj-dev libgdal-dev
$ sudo apt build-dep python-geopandas scipy
$ pip install --force-reinstall --ignore-installed --no-binary shapely pygeos -r requirements.txt 
 
```

 to make sure all system gdal, etc libraries are up to date.

 Rebuilding all is unfortunately necessary because of system projection funtimes.
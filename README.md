# EpigraphyScraperNotebook


By: Brian Ballsun-Stanton, Petra Heřmánková, and Ray Laurence

Scrapes, tabulates, and renders on a map data from (Epigraphik-Datenbank  Clauss / Slaby
EDCS)[http://db.edcs.eu/epigr/epi.php?s_sprache=en] by Manfred Clauss / Anne Kolb / Wolfgang A. Slaby / Barbara Woitas



## To run the notebook on myBinder:

Click here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mqAncientHistory/EpigraphyScraperNotebook/HEAD?urlpath=notebooks/EpigraphyScraper.ipynb)

When it starts, click the fast-forward button, or choose the Kernel menu and choose "Restart & Run All"

To run on your local system

## To run locally:

`docker build https://github.com/mqAncientHistory/EpigraphyScraperNotebook.git -t epigraphyscraper && docker run -it -p 8866:8888 epigraphyscraper`

`http://127.0.0.1:8866/notebooks/EpigraphyScraper.ipynb`

## To build locally:

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

Then rerun all cells.

Running `voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb ` may provide a cleaner UI than Jupyter Lab, if it works.


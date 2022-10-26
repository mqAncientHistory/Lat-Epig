#Download base image ubuntu 20.04
#https://www.howtoforge.com/tutorial/how-to-create-docker-images-with-dockerfile/
#FROM osgeo/proj:sha-9d4aa1fb
#FROM osgeo/gdal:ubuntu-full-latest@sha256:190726a777cb30d9700bf2a68fe54104f0890575b5c96d190fa4a5cf172242b0
#FROM python:3.9
#FROM node:16
FROM ubuntu:22.04

# FROM jupyter/scipy-notebook:016833b15ceb
# FROM armandokeller/cartopy:first
LABEL maintainer="brian.ballsun-stanton@mq.edu.au"
LABEL version="0.1"
LABEL description="Docker image for epig scraper with map generation."
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
# Update Ubuntu Software repository
# https://askubuntu.com/a/769429


RUN sed -i '/^#\sdeb-src /s/^#//' "/etc/apt/sources.list" && \
apt-get update && \
# apt-get install curl gnupg ca-certificates -y --no-install-recommends && \
apt-get install -y --no-install-recommends \
curl \
gnupg \
ca-certificates \
apt-transport-https \
apt-utils \
build-essential \
curl \
git \
libbz2-dev \
libc6 \
libffi-dev \
libgcc-s1 \
liblzma-dev \
libncurses5-dev \
libreadline-dev \
libsqlite3-dev \
libssl-dev \
libstdc++6 \
libxml2-dev \
libxmlsec1-dev \
libxslt-dev \
make \
openssh-client \
wget \
nodejs \
zlib1g-dev \
python3  \
python3-dev \
python3-cartopy \
python3-shapely \
python3-pyshp \
python3-numpy \
python3-rasterio \
python3-gdal \
cython3 \
python3-wheel \
libproj-dev \
proj-bin \
proj-data \
geos-bin \
gdal-bin \
gdal-data \
libgdal-dev \
libgeos-dev \
tini \
python3-pip && \
update-ca-certificates 

# nodejs \
# curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \


USER root

COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions


ARG NB_USER=jovyan

RUN useradd -m ${NB_USER}
ENV PYTHONPATH "/home/jovyan/work/"
ENV PATH="/home/jovyan/work/:/home/jovyan/.local/bin/:${PATH}"

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

COPY . ${HOME}

WORKDIR ${HOME}
# ENTRYPOINT ["/bin/bash"]

# RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && eval "$(pyenv init -)" && pyenv install 3.8.7 && pyenv global 3.8.7 
# RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && pip3 -q install pip --upgrade && pyenv which python && pip3 install --no-cache-dir cython numpy --no-binary :all: && pip3 install --no-cache-dir --upgrade -r requirements.txt --no-binary :all:



# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
# ENV TINI_VERSION v0.19.0
# ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
# RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "-g",  "--"]
# https://github.com/jupyter-widgets/ipywidgets/issues/1683#issuecomment-328952119


#RUN python3 -m pip install --user   --no-cache-dir cython wheel 
#RUN python3 -m pip install --user pyshp --no-cache-dir --no-binary pyshp==2.2.0
#RUN python3 -m pip install --user  shapely --no-cache-dir --no-binary shapely==1.8.1.post1
#RUN python3 -m pip install --user  cartopy --no-cache-dir --no-binary cartopy==0.20.2
RUN python3 -m pip install  pygeos --no-cache-dir --no-binary pygeos==0.13.0 && \
python3 -m pip install --user  --no-cache-dir -r requirements.txt && \
python3 -m pip install --user  --no-cache-dir --editable . && \
bash ./setupJupyter.sh && \
chown -R ${NB_USER} ${HOME}

USER ${NB_USER}

#RUN pip3 install --upgrade frictionless geoplot jupyterlab jupyter_client pandas geopandas && jupyter nbextension enable --py widgetsnbextension --sys-prefix && jupyter labextension install @jupyter-widgets/jupyterlab-manager
#RUN pip3 install ipywidgets frictionless \
#  && jupyter nbextension enable --py widgetsnbextension --sys-prefix \
#  && jupyter labextension install @jupyter-widgets/jupyterlab-manager

ENV JUPYTER_ENABLE_LAB=yes

RUN jupyter trust EpigraphyScraper.ipynb Map.ipynb

#CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "Epigraphy Scraper.ipynb"]
#voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb 

#https://github.com/ideonate/jhsingle-native-proxy/blob/master/docker-examples/jupyterhub-singleuser-voila-native/Dockerfile
EXPOSE 8888/tcp

#CMD ["jupyter", "notebook", "--ServerApp.ip='*'", "--ServerApp.token=''", "--ServerApp.password=''",  "--no-browser"]

# https://github.com/jupyter/docker-stacks/blob/main/base-notebook/Dockerfile

USER root
COPY jupyter_notebook_config.py /etc/jupyter/


# RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
#     /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
#     fix-permissions /etc/jupyter/
USER ${NB_USER}

#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser"]

CMD ["jupyter-notebook", "--NotebookApp.ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''", "--no-browser"]

RUN echo "The Notebook should now be running. If you have built this locally, visit http://localhost:8888. "
# , \     
# 	 "--VoilaConfiguration.base_url={base_url}/", \
# 	 "--VoilaConfiguration.server_url=/"]

# CMD ["voila", "--enable_nbextensions=True", \
#      "--no-browser", \
#      "--port=8888", \
#      "--VoilaConfiguration.file_whitelist=['.*']",\
#      "EpigraphyScraper.ipynb"]
# CMD ["jhsingle-native-proxy", "--destport", "8505", \
# 	 "voila", "/home/jovyan/EpigraphyScraper.ipynb", \

# We don't need to run voila as a server, since it "Voilà can also be used as a notebook server extension, both with the notebook server or with the jupyter_server."
#CMD ["bash", "runVoila.sh"]
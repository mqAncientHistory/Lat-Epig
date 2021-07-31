#Download base image ubuntu 20.04
#https://www.howtoforge.com/tutorial/how-to-create-docker-images-with-dockerfile/
FROM ubuntu:20.04
FROM python:3.9.6-buster
# FROM jupyter/scipy-notebook:016833b15ceb
# FROM python:3.8
# FROM armandokeller/cartopy:first
# FROM node:15.8.0-alpine3.10
LABEL maintainer="brian.ballsun-stanton@mq.edu.au"
LABEL version="0.1"
LABEL description="Docker image for epig scraper with map generation."
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
# Update Ubuntu Software repository
# https://askubuntu.com/a/769429
RUN sed -i '/^#\sdeb-src /s/^#//' "/etc/apt/sources.list"


RUN apt-get update
# RUN apt-get install -y --no-install-recommends \
# apt-transport-https \
# apt-utils \
# build-essential \
# ca-certificates \
# curl \
# git \
# libbz2-dev \
# libffi-dev \
# libgeos++-dev \
# liblzma-dev \
# libncurses5-dev \
# libproj-dev \
# libreadline-dev \
# libsqlite3-dev \
# libssl-dev \
# libxml2-dev \
# libxmlsec1-dev \
# make \
# proj-bin \
# proj-data \
# python3-pip \
# wget \
# zlib1g-dev \
# libgeos-dev \
# libxml2-dev \
# libxslt-dev \
# python-dev \
# libc6 \
# libgcc-s1 \
# libgeos-c1v5 \
# libproj15 \
# libstdc++6 \
# libpython3.9-dev \
# python3.9 \
# python3.9-tk


RUN apt-get install -y --no-install-recommends \
apt-transport-https \
apt-utils \
build-essential \
ca-certificates \
curl \
git \
libbz2-dev \
libffi-dev \
libgeos++-dev \
liblzma-dev \
libncurses5-dev \
libproj-dev \
libreadline-dev \
libsqlite3-dev \
libssl-dev \
libxml2-dev \
libxmlsec1-dev \
make \
proj-bin \
proj-data \
wget \
zlib1g-dev \
libgeos-dev \
libxml2-dev \
libxslt-dev \
python-dev \
libc6 \
libgeos-c1v5 \
libproj-dev \
libstdc++6


RUN update-ca-certificates

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y --no-install-recommends  nodejs



# jupyter-notebook \
# python3-bs4 \
# python3-cartopy \
# python3-clint \
# python3-geopy \
# python3-mechanicalsoup \
# python3-numpy \
# python3-pandas \
# python3-pyshp \
# python3-rtree \
# python3-tk \
# python3-shapely \
# python3-ipywidgets \
# python3-matplotlib \
# nodejs \
# npm \
# jupyter-core \
# jupyter-client \

#RUN apt-get build-dep python3-cartopy python3-lxml jupyter-notebook -y 


# RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
# 	cd ~/.pyenv && \
# 	src/configure && make -C src && \
# 	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile && \
# 	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile && \
# 	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
# 	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
	# echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile && \
	# echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc 

 
# 
# 
# RUN rm -rf /var/lib/apt/lists/* && \
# 	apt-get clean

# https://u.group/thinking/how-to-put-jupyter-notebooks-in-a-dockerfile/

# RUN mkdir src
# WORKDIR src/


USER root

ARG NB_USER=jovyan

RUN useradd -m ${NB_USER}

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

COPY . ${HOME}

WORKDIR ${HOME}

# RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && eval "$(pyenv init -)" && pyenv install 3.8.7 && pyenv global 3.8.7 
# RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && pip3 -q install pip --upgrade && pyenv which python && pip3 install --no-cache-dir cython numpy --no-binary :all: && pip3 install --no-cache-dir --upgrade -r requirements.txt --no-binary :all:


# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
# https://github.com/jupyter-widgets/ipywidgets/issues/1683#issuecomment-328952119


RUN pip3 install --no-cache-dir numpy==1.21.0 cython wheel
# jhsingle-native-proxy>=0.0.10
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN pip install --editable .
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
	jupyter contrib nbextension install --sys-prefix && \
	jupyter nbextension enable init_cell/main && \
	jupyter labextension install @voila-dashboards/jupyterlab-preview && \
	jupyter serverextension enable voila --sys-prefix


#&& \
#	jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
#	jupyter labextension install @voila-dashboards/jupyterlab-preview && \
#	jupyter serverextension enable voila --sys-prefix && \


RUN chown -R ${NB_USER} ${HOME}
USER ${NB_USER}

#RUN pip3 install --upgrade frictionless geoplot jupyterlab jupyter_client pandas geopandas && jupyter nbextension enable --py widgetsnbextension --sys-prefix && jupyter labextension install @jupyter-widgets/jupyterlab-manager
#RUN pip3 install ipywidgets frictionless \
#  && jupyter nbextension enable --py widgetsnbextension --sys-prefix \
#  && jupyter labextension install @jupyter-widgets/jupyterlab-manager

ENV JUPYTER_ENABLE_LAB=yes

RUN jupyter trust EpigraphyScraper.ipynb 

#CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "Epigraphy Scraper.ipynb"]
#voila --enable_nbextensions=True  --VoilaConfiguration.file_whitelist="['.*']" EpigraphyScraper.ipynb 

#https://github.com/ideonate/jhsingle-native-proxy/blob/master/docker-examples/jupyterhub-singleuser-voila-native/Dockerfile
EXPOSE 8888
EXPOSE 8866

#CMD ["jupyter", "notebook", "--ip='*'", "--NotebookApp.token=''", "--NotebookApp.password=''",  "--no-browser"]

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

CMD ["runVoila.sh"]
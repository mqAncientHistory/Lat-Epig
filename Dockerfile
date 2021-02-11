#Download base image ubuntu 20.04
#https://www.howtoforge.com/tutorial/how-to-create-docker-images-with-dockerfile/
FROM ubuntu:20.04
# FROM python:3.8
LABEL maintainer="brian.ballsun-stanton@mq.edu.au"
LABEL version="0.1"
LABEL description="Docker image for epig scraper with map generation."
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
# Update Ubuntu Software repository
# https://askubuntu.com/a/769429
RUN sed -i '/^#\sdeb-src /s/^#//' "/etc/apt/sources.list"
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils git build-essential make libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev proj-bin proj-data libgeos++-dev libproj-dev apt-transport-https ca-certificates
RUN update-ca-certificates
RUN apt-get upgrade -y
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
	cd ~/.pyenv && \
	src/configure && make -C src && \
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile && \
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile && \
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile && \
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc 

 
RUN apt-get build-dep -y python3-lxml python3-shapely python3-cartopy jupyter-notebook \
				python3.8 python3-cartopy jupyter-notebook \
				python3-numpy python3-numpy python3-shapely \
				python3-pyshp python3-geopandas
RUN rm -rf /var/lib/apt/lists/* && \
	apt-get clean

# https://u.group/thinking/how-to-put-jupyter-notebooks-in-a-dockerfile/
RUN mkdir src
WORKDIR src/
COPY . .
RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && eval "$(pyenv init -)" && pyenv install 3.8.7 && pyenv global 3.8.7 
RUN export PYENV_ROOT="$HOME/.pyenv" && export PATH="$PYENV_ROOT/bin:$PATH" && exec $SHELL && pip3 -q install pip --upgrade && pyenv which python && pip3 install --no-cache-dir cython numpy --no-binary :all: && pip3 install --no-cache-dir --upgrade -r requirements.txt --no-binary :all:


# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "Epigraphy Scraper.ipynb"]
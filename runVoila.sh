#!/usr/bin/env bash
#https://github.com/torressa/jupyter-stacks-voila/blob/master/docker/run_voila

python3 -m voila \
	--enable_nbextensions=True \
	--autoreload=True \
	--no-browser \
	--MappingKernelManager.cull_interval=60 \
	--MappingKernelManager.cull_idle_timeout=120 \
	EpigraphyScraper.ipynb
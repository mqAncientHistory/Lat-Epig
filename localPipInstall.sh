#!/usr/bin/env bash


python3 -m pip install numpy==1.21.1 cython wheel pyshp==2.1.3
python3 -m pip install shapely  --no-binary shapely==1.7.1 
python3 -m pip install -r requirements.txt 
python3 -m pip install  --editable . 
bash ./setupJupyter.sh 
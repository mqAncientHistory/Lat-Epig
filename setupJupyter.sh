#!/usr/bin/env bash

echo "nbextension"
jupyter nbextension enable --py widgetsnbextension --sys-prefix 
echo "contrib"
jupyter contrib nbextension install --sys-prefix 
echo "init_Cell"
jupyter nbextension enable init_cell/main 
echo "dashboards"

jupyter nbextension install --py --user hide_code
jupyter nbextension enable --py --user hide_code
jupyter serverextension enable --py --user hide_code
echo "hide_code"

#jupyter labextension install @voila-dashboards/jupyterlab-preview 
#echo "serverextension"
# jupyter serverextension enable voila --sys-prefix
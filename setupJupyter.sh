#!/usr/bin/env bash

echo "nbextension"
jupyter nbextension enable --py widgetsnbextension --sys-prefix 
echo "contrib"
jupyter contrib nbextension install --sys-prefix 
echo "init_Cell"
jupyter nbextension enable init_cell/main 
echo "dashboards"
#jupyter labextension install @voila-dashboards/jupyterlab-preview 
#echo "serverextension"
jupyter serverextension enable voila --sys-prefix
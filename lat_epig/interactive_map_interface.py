from lat_epig.interactive_map import make_interactive_map
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks


import shutil
import datetime
import glob
import re

import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path
from yaspin import yaspin

#https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/
SUPPORTING_DATA = Path("awmc.unc.edu")
SUPPORTING_DATA = SUPPORTING_DATA / "awmc" / "map_data" / "shapefiles"
PROVINCES_SHP   = SUPPORTING_DATA / "political_shading" 
OUTPUTS = Path("output")
class Parseargs:
    maps = None


def make_i_map_interface():
    args = Parseargs()
    i_map_button = widgets.Button(description="Refresh Interactive Map!" ,
        layout={'width': 'max-content'})
    #     map_button_interactive = widgets.Button(description="Reload Interactive!")
    out = widgets.Output(layout={'border': '1px solid black'})
#     display(HTML("<h1>Interactive Map</h1>"))
#     display(HTML("<h2>Choose datafiles to plot</h2>"))
#     display(HTML("<h2>Map viewer</h2>"), map_button_interactive)
    
    def interactive_refresh(b):
        # https://stackoverflow.com/a/38797877
        LDN_COORDINATES = (51.5074, 0.1278) 
        m = folium.Map(location=LDN_COORDINATES, zoom_start=12)
        #m._build_map()
        #mapWidth, mapHeight = (400,500) # width and height of the displayed iFrame, in pixels
        #srcdoc = m.HTML.replace('"', '&quot;')
        #embed = HTML('<iframe srcdoc="{}" '
        #             'style="width: {}px; height: {}px; display:block; width: 50%; margin: 0 auto; '
        #             'border: none"></iframe>'.format(srcdoc, width, height))
        display(m)
        
    

    i_map_refresh=widgets.Button(
        description="Update Data File List",
        layout={'width': 'max-content'}
    )

    def get_outputs():
        outputs = {}
        for output in OUTPUTS.glob("*.tsv"):
            outputs[output.stat().st_mtime] = (output.name, output)
        output_keys = sorted(outputs, reverse=True)
        
        filenames = []
        for key in output_keys:
            filenames.append(outputs[key])
        
        
        return filenames
    def i_reset_outputs(b):
        i_map_data.options=get_outputs()

    i_map_data=widgets.Dropdown(
        description="Data File",
        options=get_outputs(),
        layout={'width': 'max-content'}
        )



    
    display(HTML("<h1>Interactive Map</h1>"), i_map_refresh, i_map_data, i_map_button)
    display(HTML("<h2>Interactive Map Output</h2>"), out)    
    
    def i_map_on_button_clicked(b):
        with out:
            if not i_map_data.value:
                display("<span style='color:red'>No data scraped</span>")
                return
            out.clear_output(wait=True)
            i_map = make_interactive_map(i_map_data.value)
            out.clear_output(wait=True)
            display(i_map)
        

    i_map_button.on_click(i_map_on_button_clicked)
    i_map_refresh.on_click(i_reset_outputs)
#     map_button_interactive.on_click(interactive_refresh)
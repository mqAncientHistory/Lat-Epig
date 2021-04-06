import make_map 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks

import shutil
import datetime
import glob


import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling

#https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/



class Parseargs:
    maps = None

def make_map_interface():
    args = Parseargs()
    map_button = widgets.Button(description="Generate New Maps!")
    map_button_interactive = widgets.Button(description="Reload Interactive!")
    out = widgets.Output(layout={'border': '1px solid black'})
    display(HTML("<h1>Interactive Map</h1>"))
    display(HTML("<h2>Choose datafiles to plot</h2>"))
    display(HTML("<h2>Map viewer</h2>"), map_button_interactive)
    
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
        
    
    
    display(HTML("<h1>Generate PDF Map</h1>"), map_button, out)
    def map_on_button_clicked(b):
        with out:
            display(HTML("<p>Starting Map Generation</p>"))
            
        with out:           
            make_map.main()
            datestring=datetime.datetime.now().strftime("%Y%m%d")
            output_filename=f"epigraphy_scraper_maps_output_{datestring}"
            shutil.make_archive(output_filename, 'zip', "output_maps/")
            output_tsv_filename=f"epigraphy_scraper_spreadsheet_output_{datestring}"
            shutil.make_archive(output_tsv_filename, 'zip', "already_mapped_data/output/")
            # display(HTML("<a href='/tree/output_maps/' target='_blank'>Full Maps</a>"))
            display(HTML("<ul>"))
            # for zipfile in glob.glob("output_maps/*.pdf"):
            #     display(HTML(f"<li><a href='/tree/{zipfile}'>{zipfile}</a></li>"))
            for zipfile in glob.glob("*.zip"):
                display(HTML(f"<li><a href='{zipfile}'>{zipfile}</a></li>"))
            display(HTML("</ul>"))
    map_button.on_click(map_on_button_clicked)
    map_button_interactive.on_click(interactive_refresh)
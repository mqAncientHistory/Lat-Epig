from lat_epig.make_map import make_map
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

#https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/
SUPPORTING_DATA = Path("awmc.unc.edu")
SUPPORTING_DATA = SUPPORTING_DATA / "awmc" / "map_data" / "shapefiles"
PROVINCES_SHP   = SUPPORTING_DATA / "political_shading" 
OUTPUTS = Path("output")
class Parseargs:
    maps = None

def make_map_interface():
    args = Parseargs()
    map_button = widgets.Button(description="Generate New Maps!")
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
        
    

    map_refresh=widgets.Button(
        description="Update Data File List"
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
    def reset_outputs(b):
        map_data.options=get_outputs()

    map_data=widgets.Dropdown(
        description="Data File",
        options=get_outputs(),
        layout=Layout(width='50%')
        )

    map_title=widgets.Text(
        description='Map Title:'
    ) 

    province_list=[]
    for province in PROVINCES_SHP.glob("roman_empire_*.shp"):
        province_list.append((str(province.name).replace(".shp", "").replace("ad","AD").replace("bc","BC").replace("roman_","").replace("empire_","").replace("_"," ") ,
                              province.name))

    #print(province_list)



    map_shapefile=widgets.Dropdown(
        description="Basemap",
        value="roman_empire_ad_117.shp",
        options=province_list
        )
    map_show_roads = widgets.RadioButtons(
        options=[("All Roman Roads", 'all'),
                 ("Roads around points", "points"),
                 ("No Roads", None)],
        value="all",
        description="Show Roads")

    map_show_cities = widgets.RadioButtons(
        options=[("All Cities", 'all'),
                 ("Cities around points", "points"),
                 ("No Cities", None)],
        value="all",
        description="Show Cities")


    map_basemap_multicolour = widgets.RadioButtons(
        options=[('Light Brown', False), ('Multicoloured', True)],
        value=True,
        description="Basemap<br/>Styling"
        )
    
    display(HTML("<h1>Generate PDF Map</h1>"), map_refresh, map_data, map_title, map_shapefile, map_basemap_multicolour, map_show_roads, map_show_cities, map_button, out)
    def map_on_button_clicked(b):

        if map_title.value:
            map_title_text=map_title.value
        else:
            map_title_text=None

        
        


        with out:
            display(HTML("<p>Starting Map Generation</p>"))
            
        with out:
            searchterm=None            
            # for term in map_data.value.name.split("+"):
            #     if "term1" in term:
            #         searchterm = re.search("term1_(.*)-[0-9].*", term).group(1)
            # if searchterm == "%":
            #     searchterm=None

            make_map(data_file=map_data.value,
                     map_title_text=map_title_text,
                     province_shapefilename=map_shapefile.value,
                     basemap_multicolour=map_basemap_multicolour.value,
                     searchterm=searchterm,
                     provinces=True,
                     roads=map_show_roads.value,
                     cities=map_show_cities.value
                     )
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
    map_refresh.on_click(reset_outputs)
#     map_button_interactive.on_click(interactive_refresh)
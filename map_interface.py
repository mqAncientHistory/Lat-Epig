import make_map 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks

import shutil
import datetime

class Parseargs:
    maps = None

def make_map_interface():
    args = Parseargs()
    map_button = widgets.Button(description="Generate New Maps!")
    display(HTML("<h1>Mapper</h1>"), map_button)
    def map_on_button_clicked(b):
 	    with widgets.Output(layout={'border': '1px solid black'}) as out:

	        display("Starting Map Generation")
	        make_map.main()
	        datestring=datetime.datetime.now().strftime("%Y%m%d")
	        output_filename=f"epigraphy_scraper_maps_output_{datestring}.zip"
	        shutil.make_archive(output_filename, 'zip', ["already_mapped_data/", "output_maps/"])
	        display(HTML("<a href='/tree/output_maps/' target='_blank'>Full Maps</a>"))
	        display(FileLink(output_filename))

    map_button.on_click(map_on_button_clicked)
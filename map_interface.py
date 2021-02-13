import make_map 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks

import shutil
import datetime
import glob

class Parseargs:
    maps = None

def make_map_interface():
    args = Parseargs()
    map_button = widgets.Button(description="Generate New Maps!")
    out = widgets.Output(layout={'border': '1px solid black'})
    display(HTML("<h1>Mapper</h1>"), map_button, out)
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
import make_map 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks

class Parseargs:
    maps = None

def make_map_interface():
    args = Parseargs()
    map_button = widgets.Button(description="Generate New Maps!")
    display(HTML("<h1>Mapper</h1>"), map_button)
    def map_on_button_clicked(b):
        print("Starting Map Generation")
        make_map.main()
    map_button.on_click(map_on_button_clicked)
import parse 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks
import threading
import glob

class Parseargs:
    
    EDCS = None
    publication = None
    province = []
    provincelist = [None, "Achaia", "Aegyptus", "Africa Proconsularis", "Alpes Cottiae",  "Alpes Graiae", "Alpes Maritimae", "Alpes Poeninae", "Apulia et Calabria / Regio II", "Arabia", "Armenia", "Asia", "Baetica", "Barbaricum", "Belgica", "Britannia", "Bruttium et Lucania / Regio III", "Cappadocia", "Cilicia", "Corsica", "Creta et Cyrenaica", "Cyprus", "Dacia", "Dalmatia", "Etruria / Regio VII", "Galatia", "Gallia Narbonensis", "Germania Inferior", "Germania Superior", "Hispania Citerior", "Italia", "Latium et Campania / Regio I", "Liguria / Regio IX", "Lugudunensis", "Lusitania", "Lycia et Pamphylia", "Macedonia", "Mauretania Caesariensis", "Mauretania Tingitana", "Mesopotamia", "Moesia Inferior", "Moesia Superior", "Noricum", "Numidia", "Palaestina", "Pannonia inferior", "Pannonia Superior", "Picenum / Regio V", "Pontus et Bithynia", "Provincia incerta", "Raetia", "Regnum Bospori", "Roma Aemilia / Regio VIII", "Samnium / Regio IV", "Sardinia", "Sicilia", "Syria", "Thracia", "Transpadana / Regio XI", "Umbria / Regio VI Aquitani(c)a", "Venetia et Histria / Regio X" ]
    place = None
    term1 = None
    operator = "and"
    operatorlist = ["and", "or", "not"]
    term2 = None
    dating_from = None
    dating_to = None
    inscription_genus = []
    and_not_inscription_genus = []
    debug = False
    from_file = None
    to_file = None
    genus_list = [None, 
"Augusti/Augustae",
"carmina", 
"inscriptiones christianae", 
"leges",
"liberti/libertae", 
"litterae erasae", 
"litterae in litura", 
"miliaria",
"militaria", 
"milites",
"mulieres", 
"nomen singulare",
"officium/professio",
"ordo decurionum", 
"ordo equester", 
"ordo senatorius", 
"praenomen et nomen defixiones",
"reges diplomata",  
"sacerdotes christiani",
"sacerdotes pagani",
"servi/servae", 
"seviri Augustales",
"sigilla impressa",
"signacula medicorum", 
"termini",
"tituli fabricationis", 
"tituli honorarii",
"tituli operum", 
"tituli possessionis", 
"tituli sacri",
"tituli sepulcrales",
"tria nomina miliaria",
"viri senatus consulta"
]

def makeScrapeInterface():

    args = Parseargs()

    
    term1=widgets.Text(
        description='Text 1:'
    ) 
    operator=widgets.ToggleButtons(
        options=Parseargs.operatorlist,
        value="and",

        description='Operator'
    ) 

    
    term2=widgets.Text(
        description='Text 2:'
    ) 
    

    
    EDCS=widgets.Text(
        description='EDCS-ID:'
    ) 
    
    publication=widgets.Text(
        description='Publication:'
    ) 
    
    
   
    
    
    province=widgets.SelectMultiple(
        options=Parseargs.provincelist,
        rows=10,
        description='Province:'
    ) 
    place=widgets.Text(
        description='Place:'
    ) 
    
    
    
    

    dating_from=widgets.Text(
        description='dating from:'
    ) 
    
    
    
    dating_to=widgets.Text(
        description='dating to:'
    ) 
    

    inscription_genus=widgets.SelectMultiple(
        options=Parseargs.genus_list,
        rows=10,
        description='inscription genus / personal status:'
    ) 
    

    and_not_inscription_genus=widgets.SelectMultiple(
        options=Parseargs.genus_list,
        rows=10,
        description='and not:'
    ) 
    
    inscription_genus.layout.display='none'
    and_not_inscription_genus.layout.display='none'

            
    genus_button = widgets.Button(description="Inscription Genus...")

    button = widgets.Button(description="Scrape!")
    
    out = widgets.Output(layout={'border': '1px solid black'})

    display(HTML("<h1>Scraper</h1>"), term1, operator, term2, EDCS,publication, place, dating_from, dating_to, HTML("<div>Shift or Control click to select multiple in these lists</div>"),province, genus_button, inscription_genus, and_not_inscription_genus, button, out)
    
    
    
    def on_button_clicked(b):
        with out:
            if and_not_inscription_genus.value:
                args.and_not_inscription_genus=and_not_inscription_genus.value

            if dating_from.value:
                args.dating_from=dating_from.value

            if dating_to.value:
                args.dating_to=dating_to.value

            if EDCS.value:
                args.EDCS=EDCS.value

            if inscription_genus.value:
                args.inscription_genus=inscription_genus.value

            if operator.value:
                args.operator=operator.value

            if place.value:
                args.place=place.value

            if province.value:
                args.province=province.value

            if province.value:
                args.province=province.value

            if publication.value:
                args.publication=[publication.value]

            if term1.value:
                args.term1=term1.value

            if term2.value:
                args.term2=term2.value


         #   with widgets.Output(layout={'border': '1px solid black'}) as out:

            display(HTML("<p>Starting Scrape. This may take a few minutes, depending on the number of search results.</p>"))

            filename=parse.scrape(args)
            #print(filename)
            # display(HTML("<a href='/tree/output/' target='_blank'>Full File List</a>"))
            display(HTML("<ul>"))
            for zipfile in glob.glob("output/*.tsv"):
                display(HTML(f"<li><a href='{zipfile}'>{zipfile}</a></li>"))
            display(HTML("</ul>"))
    
    def genusbutton(on_button_clicked):
        genus_button.layout.display='none'
        inscription_genus.layout.display='flex'
        and_not_inscription_genus.layout.display='flex'
    
    genus_button.on_click(genusbutton) 
    button.on_click(on_button_clicked)

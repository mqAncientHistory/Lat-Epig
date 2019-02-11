import parse 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.core.display import display, HTML
from IPython.display import FileLink, FileLinks

class Parseargs:
    
    EDCS = None
    publication = None
    province = []
    provincelist = [None, "Achaia", "Baetica", "Barbaricum", "Belgica", "Britannia", "Bruttium et Lucania / Regio III", "Cilicia", "Corsica", "Creta et Cyrenaica", "Cyprus", "Dacia", "Dalmatia", "Etruria / Regio VII", "Galatia", "Gallia Narbonensis", "Germania inferior", "Germania superior", "Hispania citerior", "Italia", "Latium et Campania / Regio I", "Liguria / Regio IX", "Lugudunensis", "Lusitania", "Lycia et Pamphylia", "Macedonia", "Mauretania Caesariensis", "Mauretania Tingitana", "Mesopotamia", "Moesia inferior", "Moesia superior", "Noricum", "Numidia", "Palaestina", "Pannonia inferior", "Pannonia superior", "Picenum / Regio V", "Pontus et Bithynia Armenia", "Provincia incerta Asia", "Raetia""Regnum Bospori Aegyptus", "Roma Aemilia / Regio VIII", "Samnium / Regio IV Africa proconsularis", "Sardinia Alpes Cottiae", "Sicilia Alpes Graiae","Cappadocia", "Syria Alpes Maritimae", "Thracia Alpes Poeninae", "Transpadana / Regio XI Apulia et Calabria / Regio II", "Umbria / Regio VI Aquitani(c)a", "Venetia et Histria / Regio X Arabia", ]
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
    genus_list = [None, "et", "vel", "carmina", "sigilla impressa", "Augusti/Augustae", "praenomen et nomen defixiones", "signacula medicorum", "liberti/libertae", "reges diplomata militaria", "termini", "milites", "sacerdotes christiani inscriptiones christianae", "tituli fabricationis", "mulieres", "sacerdotes pagani leges", "tituli honorarii", "nomen singulare", "servi/servae litterae erasae", "tituli operum", "officium/professio", "seviri Augustales litterae in litura", "tituli possessionis", "ordo decurionum", "tria nomina miliaria", "tituli sacri", "ordo equester", "viri senatus consulta", "tituli sepulcrales", "ordo senatorius"]

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
    
            
    
    button = widgets.Button(description="Scrape!")
    
    display(HTML("<h1>Scraper</h1>"), term1, operator, term2, EDCS,publication, place, dating_from, dating_to, HTML("<div>Shift or Control click to select multiple in these lists</div>"),province, inscription_genus, and_not_inscription_genus, button)
    
    
    
    def on_button_clicked(b):
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



        print("Starting Scrape. This may take a few minutes, depending on the number of search results.")

        filename=parse.scrape(args)
        #print(filename)
        display(HTML("<a href='/tree/output/' target='_blank'>Full File List</a>"))
        display(FileLink(filename))
        
        
    button.on_click(on_button_clicked)
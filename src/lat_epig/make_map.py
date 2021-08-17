#!/usr/bin/env python
# GPL v3 Brian Ballsun-Stanton
# Taken from https://automating-gis-processes.github.io/2016/Lesson5-static-maps.html

import datetime
import geopandas
import matplotlib.pyplot as plt
from frictionless import extract
from pathlib import Path
from pprint import pprint
import pandas
import os
import subprocess
import geoplot
import matplotlib
import shutil
import glob
# https://geopandas.org/reference/geopandas.GeoDataFrame.html#geopandas.GeoDataFrame
from shapely.geometry import Point
# https://geopandas.org/gallery/plotting_basemap_background.html#sphx-glr-gallery-plotting-basemap-background-py
import contextily as ctx

from yaspin import yaspin
from lat_epig.scalebar import scale_bar

import cartopy.crs as ccrs
import textwrap
# https://github.com/geopandas/geopandas/issues/1597
from matplotlib_scalebar.scalebar import ScaleBar
from collections import defaultdict
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


from matplotlib import cm

import psutil
import matplotlib.patheffects as pe


#from blume.table import table
#from blume.taybell import table


#https://geopython.github.io/OWSLib/#wms
#from owslib.wms import WebMapService
#from owslib.wfs import WebFeatureService

# TO DISABLE SSL CHECKING 
# $ export CURL_CA_BUNDLE=""; ./make_map.py

CITATION = 'Ballsun-Stanton B., Heřmánková P., Laurence R. "Lat Epig" (version 2.0). GitHub.\nhttps://github.com/mqAncientHistory/Lat-Epig/     https://doi.org/10.5281/zenodo.5211341'
DATA_DIR = "output"
DATA_FILENAME = "2020-08-18-term1_petra-249.tsv"
#DATA_FILE = DATA_DIR / DATA_FILENAME
DEBUG = False
SUPPORTING_DATA = Path("awmc.unc.edu")
SUPPORTING_DATA = SUPPORTING_DATA / "awmc" / "map_data" / "shapefiles"
ROMAN_ROADS_SHP = SUPPORTING_DATA / "ba_roads" / "ba_roads.shp"
#awmc.unc.edu/awmc/map_data/shapefiles/political_shading/roman_empire_ad_69_extent.sbn
PROVINCES_SHP   = SUPPORTING_DATA / "political_shading" 
#CITIES_SHP      = SUPPORTING_DATA / "strabo_data" / "straborivers_current.shp"
CITIES_DATA     = Path("cities") / "Hanson2016_Cities_OxREP.csv"
MIN_MAP = 5000



# WMS_LAYERS={"Roman Roads":{"name":'Roman Roads', "zorder":"0"},
#       "Provinces (ca. AD117)":{"name":'Provinces (ca. AD117)', "zorder":"1"},
#       "Cities and Settlements":{"name":'Cities and Settlements', "zorder":"2"},
# }
# layers_list = list(WMS_LAYERS.keys())
# https://stackoverflow.com/a/15445989
# import requests
# from urllib3.exceptions import InsecureRequestWarning

# # Suppress only the single warning from urllib3 needed.
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



# wms = WebMapService('https://ags.cga.harvard.edu/arcgis/services/darmc/roman/MapServer/WMSServer?', version='1.1.1')
# for content in wms.contents:
#   if wms[content].title in WMS_LAYERS:
#     pprint((content, wms[content], wms[content].title, wms[content].crsOptions, wms[content].styles, wms[content].boundingBoxWGS84))

#     WMS_LAYERS[wms[content].title]['wms'] = wms[content]
#https://geopandas.org/install.html



# pprint(wms.getOperationByName('GetCapabilities').methods)
# pprint(wms.getOperationByName('GetCapabilities').formatOptions)

# pprint(point_geodataframe_3857.total_bounds)
# img = wms.getmap(layers=['92'],
#                  src='EPSG:3857',
#                  size=(900,900),
#                  bbox=point_geodataframe_3857.total_bounds,
#                  format='image/png',
#                  transparent=True
#                  )


# out = open('roman-map.png', 'wb')
# out.write(img.read())
# out.close()

# https://geopandas.org/gallery/create_geopandas_from_pandas.html#sphx-glr-gallery-create-geopandas-from-pandas-py

# ax = world.plot(
#   color='white', 
#   edgecolor='black')

# https://geopandas.org/gallery/plotting_with_geoplot.html
# geoplot.polyplot(world, figsize=(8, 4))
# ax = geoplot.polyplot(
#     world, projection=geoplot.crs.Orthographic(), figsize=(10, 10)
# )
# ax.outline_patch.set_visible(True)

def makeDataframe(data_file, epsg=3857):


    
  # pprint(WMS_LAYERS)
  # pprint([op.name for op in wms.operations])

  # https://frictionlessdata.io/tooling/python/extracting-data/
  # Handles multiline columns cleanly.
  data_filename = os.path.basename(data_file)
  import_rows = extract(data_file)
  import_dataframe = pandas.DataFrame(import_rows)

  #cities_3857 = geopandas.read_file(CITIES_SHP).to_crs(epsg=3857)

  point_geodataframe = geopandas.GeoDataFrame(
  import_dataframe[import_dataframe.Longitude.notnull()],
  geometry=geopandas.points_from_xy(
    import_dataframe[import_dataframe.Longitude.notnull()].Longitude,
    import_dataframe[import_dataframe.Longitude.notnull()].Latitude),
  crs="EPSG:4326")
  if DEBUG:
    pprint(point_geodataframe)

  point_geodataframe_3857 = point_geodataframe.to_crs(epsg=epsg)
  return point_geodataframe_3857

@yaspin(text="Making maps...")
def make_map(data_file, 
             map_title_text=None, 
             province_shapefilename="roman_empire_ad_117.shp",
             searchterm=None, 
             basemap_multicolour=True, 
             provinces=True, 
             roads=True, 
             cities=True,
             filetype='pdf',
             show_ids=False,
             append_inscriptions=False,
             dpi=1200,
             map_dimensions=None,
             partial_provinces=False,
             map_inscription_markersize=5,
             map_greyscale=False, 
             will_cite=False):


  
  if not os.path.exists('output_maps'):
    os.makedirs('output_maps')

  cities_rows = extract(CITIES_DATA)
  cities_dataframe = pandas.DataFrame(cities_rows)


  #https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/

  roads_3857 = geopandas.read_file(ROMAN_ROADS_SHP).to_crs(epsg=3857)
  provinces_3857 = geopandas.read_file(PROVINCES_SHP / province_shapefilename).to_crs(epsg=3857)


  cities_geodataframe_3857 = geopandas.GeoDataFrame(
    cities_dataframe,
    geometry=geopandas.points_from_xy(
      cities_dataframe["Longitude (X)"],
      cities_dataframe["Latitude (Y)"]),
    crs="EPSG:4326").to_crs(epsg=3857)

  geopandas.options.use_pygeos = True

  point_dataframe_3857 = makeDataframe(data_file)

  print("Loaded data...")
  #pprint(point_dataframe_3857[["geometry", "Longitude", "Latitude" ]])
  #print(f"Making {data_file}\n\troads: {roads}\n\tprovinces: {provinces}\n\tcities: {cities}\n")



  fig = plt.figure(figsize=map_dimensions, dpi=dpi)

  if map_greyscale:
    print("greyscale")
    plt.style.use('grayscale')
 
  ax = fig.add_subplot(1,1,1, projection=ccrs.Mercator.GOOGLE, frameon=False)

  ax = plt.axes(projection=ccrs.Mercator.GOOGLE)
 
  ax.axis('off')
  ax.coastlines(resolution='10m', linewidth=0.05)

  #https://geopandas.org/gallery/plotting_with_geoplot.html
  world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
  # ax = geoplot.polyplot(
  #     world, 
  #     #projection=geoplot.crs.Orthographic(), 
  #     figsize=(8, 4)
  # )
  if not map_title_text:  
    map_title_text = data_file.name.replace("-"," ").replace("_"," ").replace(".tsv","")
  
  map_metadata_list=data_file.name.replace(".tsv","").split("-")
  search_params = map_metadata_list[3].replace("_"," ").replace("term1","Term 1 =").replace("term2","Term 2 =").replace("%","All").replace("+","; ").replace(r" +"," ")
  escaped_provinceshapefilename = province_shapefilename.replace("_", r"_")
  map_metadata = rf"""Search Parameters: {search_params}
Results: {map_metadata_list[4]} Date scraped: {map_metadata_list[0]}-{map_metadata_list[1]}-{map_metadata_list[2]}
Data from Epigraphik-Datenbank Clauss / Slaby <http://manfredclauss.de/>
Ancient World Mapping Center “{escaped_provinceshapefilename}” <http://awmc.unc.edu/wordpress/map-files/>"""
  if not will_cite:

    fig.text(0.5, 0, CITATION,
        verticalalignment='bottom', horizontalalignment='center',        
        fontsize=6)  

  

  #print(f"making map with title {map_title_text}")
  #print(f"making map with metadata {map_metadata_list} rendered as \n{map_metadata}")
  plt.tight_layout()
  plt.suptitle(map_metadata, fontsize=3, y=0.10)
  plt.title(map_title_text, fontsize=12, y=1)
  plt.rc('font',**{'family':'serif'})

  print("Initialised plot...")

  #https://gis.stackexchange.com/a/266833
  buffer = geopandas.GeoDataFrame(geometry=point_dataframe_3857.buffer(MIN_MAP, cap_style = 3))

  xmin, ymin, xmax, ymax = buffer.total_bounds


  #pprint((xmin, ymin, xmax, ymax, buffer.total_bounds, point_dataframe_3857.total_bounds))

  #THIS PROBABLY IS WRONG, BUT IT MAKES A MAP?!
  # print("Currently used memory:", psutil.virtual_memory().percent)

  if not partial_provinces:
    #    print("entering low-memory province mode", partial_provinces, psutil.virtual_memory().percent > 60)
    bounded_prov = provinces_3857.cx[xmin:xmax, ymin:ymax]
  else:
    bounded_prov = provinces_3857#geopandas.overlay(buffer, provinces_3857, how='union', keep_geom_type=False)
  
  # print("Currently used memory:", psutil.virtual_memory().percent)
  province_shapefilename=province_shapefilename.replace("_provinces.shp", "").replace("ad","AD").replace("bc","BC").replace("roman_","").replace("empire_","").replace("_"," ")
  province_shapefilename=f"Provinces in {province_shapefilename}"
  #pprint(province_shapefilename)
  if provinces:
    prism = plt.get_cmap("prism")
    brown = "#C39B77"
    red = "#ff0000"
    if map_greyscale:      
      #rgb = cm.get_cmap(plt.get_cmap("prism"))(bounded_prov)[np.newaxis, :, :3]
      prism =  ListedColormap(["#eeeeee", "#111111", "#bbbbbb", "#333333", "#999999","#000000","#ffffff", "#777777"])
      brown = '#9d9d9d'
      red = '#000000'
    if basemap_multicolour:
      bounded_prov.plot(ax=ax, linewidth=1, alpha=0.1,  cmap=prism, zorder=1, label=province_shapefilename)
    else:
      bounded_prov.plot(ax=ax, linewidth=0.3, alpha=0.5, color=brown, linestyle='dashed', zorder=1, label=province_shapefilename)
    print("Plotted provinces...")
  if roads:
    if roads == "points":
      bounded_roads = roads_3857.cx[xmin:xmax, ymin:ymax]
    else:
      bounded_roads = roads_3857
    bounded_roads.plot(ax=ax, linewidth=0.2, alpha=1,  color='gray', zorder=2, label="Roads")
    print("Plotted roads...")

  if cities:
    if cities == "points":
      bounded_cities = cities_geodataframe_3857.cx[xmin:xmax, ymin:ymax]
    else:
      bounded_cities = cities_geodataframe_3857
    bounded_cities.plot(ax=ax, marker="+", markersize=2, linewidth=0.25, alpha=0.25,  color='black', zorder=3, label="Cities")
    print("Plotted cities...")

  if searchterm:
    searchterm = f"Inscription:\n{searchterm}"
  else:
    searchterm = "Inscriptions"
  point_dataframe_3857.plot(ax=ax
                           , marker="."
                           , linewidth=0.2
                           , markersize=map_inscription_markersize
                           , alpha=0.5
                           , color=red
                           , edgecolor='k'
                           , zorder=4
                           , label=f"{searchterm}")
  #ctx.add_basemap(ax, source=ctx.providers.Stamen.TerrainBackground)
  print("Plotted data...")

  if show_ids:
    for x,y, label in zip(point_dataframe_3857.geometry.x, point_dataframe_3857.geometry.y, point_dataframe_3857["EDCS-ID"]):
      #print(x,y,label)
      ax.annotate(label, xy=(x, y), xytext=(2, 2), textcoords="offset points", fontsize=1,
                      path_effects=[pe.withStroke(linewidth=0.5, foreground="white")])

    # https://stackoverflow.com/a/50270936
    #point_dataframe_3857.apply(lambda x: ax.annotate(s=x['EDCS-ID'], xy=x.geometry.coords[0], xytext=(3,3), textcoords="offset points"))

  legend = ax.legend(fontsize='small')
  legend.legendHandles[1]._sizes = [30]
  legend.legendHandles[2]._sizes = [30]


  # for layer in WMS_LAYERS:
  #   print("foo")
  #   current_layer = WMS_LAYERS[layer]['wms']
  #   pprint(layer)
  #   pprint(current_layer.getOperationByName('GetMap').methods)
  #   pprint(current_layer.getOperationByName('GetMap').formatOptions)

  #layermap_3857 = wms.getmap(layers=WMS_LAYERS.keys(),
  #                           srs="EPSG:3857",
  #                           )


  plt.axis('off')


  # ax.add_artist(ScaleBar(1, 
  #                        units="km", 
  #                        length_fraction=0.15, 
  #                        location="lower left", 
  #                        font_properties={"size": "xx-small"}))

  x, y, arrow_length = 0.005, 0.1, 0.075
  ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
              arrowprops=dict(facecolor='black', arrowstyle='->'),#width=.05, headwidth=2),
              ha='center', va='center', fontsize=5,
              xycoords=ax.transAxes)
  # point_geodataframe.plot(ax=ax, color='red')
  #https://stackoverflow.com/a/53735672

  # print("\n\n***\n\nBRIAN", fig.bbox, (bounded_prov.total_bounds[2] - bounded_prov.total_bounds[0]))
  if (buffer.total_bounds[2] - buffer.total_bounds[0]) < 1000000:
   scale = 100
  else:
    scale = 1_000

  scale_bar(ax, (0.05, 0.05), scale)
  ax.xaxis.set_visible(False)
  ax.set_xticks([0]) 

  ax.autoscale_view(tight=True)

  province_shapefilename=province_shapefilename.replace(" ","_").replace(".shp","")
  datafile_base_name = data_file.name.replace('.tsv','')
  map_filename=f"output_maps/{datafile_base_name}{f'-{province_shapefilename}' if provinces else ''}{f'-Cities{cities}' if cities else ''}{f'-Roads{roads}' if roads else ''}{f'-IDs' if show_ids else ''}{f'-index' if append_inscriptions else ''}{f'-multicolour' if basemap_multicolour else ''}-DPI{dpi}-{'-for_publication' if map_greyscale else ''}"
  
  
  ax.spines['geo'].set_visible(False)

  #fig.set_size_inches(11.7,8.3) # dpi=80

  #ax.get_tightbbox()
  #ax.outline_patch.set_visible(False)
  if filetype != 'pdf':
    plt.savefig(f"{map_filename}.{filetype}", dpi=dpi,bbox_inches='tight')
    plt.close()
    print("Saved map...")
  else:
    figdate = [int(x) for x in data_file.name.replace("-"," ").replace("_"," ").replace(".tsv","").split( )[0:3]]
    with PdfPages(f"{map_filename}.{filetype}", metadata={"Title":map_title_text,
                                                          "Subject":map_metadata,
                                                          "Creator":"Lat Epig by Ballsun-Stanton, Heřmánková, and Laurence",
                                                          "Keywords":' '.join(data_file.name.replace("-"," ").replace("_"," ").replace(".tsv","").split( )[3:]),
                                                          "CreationDate": datetime.datetime(figdate[0], figdate[1], figdate[2])
                                                          }) as pdf:
      #https://matplotlib.org/stable/api/backend_pdf_api.html#matplotlib.backends.backend_pdf.PdfPages
      pdf.savefig(fig, dpi=dpi,bbox_inches='tight')
      plt.close()
      print("Saved map...")
      if append_inscriptions and point_dataframe_3857.size >= 250:
        print("Too many inscriptions to attach to PDF, use your TSV instead.")
      elif append_inscriptions:
        print("Appending inscriptions...")
        def chunks(lst, n):
          # https://stackoverflow.com/a/312464
          """Yield successive n-sized chunks from lst."""
          for i in range(0, len(lst), n):
              yield lst[i:i + n]

        point_dataframe_3857["geom_4326"] = point_dataframe_3857["geometry"].to_crs("EPSG:4326")
        cell_text=point_dataframe_3857[["EDCS-ID","inscription interpretive cleaning", "province", "place", "geom_4326"]].sort_values(by='EDCS-ID').values
        #pprint(cell_text)
        # rowLabels=point_dataframe_3857[].values
        
        formatted_text={}
        for a_line in cell_text:
          geom = a_line[4]
          y=round(geom.y,2)
          x=round(geom.x,2)
          province=a_line[2]
          place=a_line[3]
          y_bucket=int(5 * round(y/5))
          x_bucket=int(5 * round(x/5))
          #print(y, y_bucket, x, x_bucket)
          key = a_line[0]
          line = a_line[1] or 'No Inscription Listed'
          if y_bucket not in formatted_text:
            formatted_text[y_bucket] = {}
          if x_bucket not in formatted_text[y_bucket]:
            formatted_text[y_bucket][x_bucket] = []
          formatted_text[y_bucket][x_bucket].append('\n'.join([textwrap.shorten(" - ({}, {}, {})".format(key, province, place), width=120)] + textwrap.wrap(line, width=100, max_lines=3, initial_indent='        ', subsequent_indent='        ' )))

        #matplotlib.rcParams['text.latex.unicode']=True
        formatted_slice = []
        
        for y_bucket in sorted(formatted_text):
          for x_bucket in sorted(formatted_text[y_bucket]):
            formatted_slice.append("\nInscriptions near Long: {}, Lat: {}".format(y_bucket, x_bucket))
            for inscription in formatted_text[y_bucket][x_bucket]:
              formatted_slice.append(inscription)


        plt.rc('font',**{'family':'serif'})
        plt.rc('text', usetex=False)

        #if len(formatted_slice) > 80:
        #  v_align='center'
        #else:
        v_align='center'
        #pprint(point_dataframe_3857)
        #https://stackoverflow.com/q/57713738
        fig = plt.figure(dpi=dpi)
        ax = fig.add_axes([0,0,1,1])
        ax.set_axis_off()
        t = ax.text(0, 0.5, "\n".join(formatted_slice), 
                horizontalalignment='left', 
                verticalalignment=v_align,
                fontsize=10, 
                color='black',
                wrap=True)
        ax.figure.canvas.draw()
        bbox = t.get_window_extent()
        #fig.set_size_inches(8.3, 11.7) # dpi=80
        fig.set_size_inches(bbox.width/dpi, bbox.height/dpi) # dpi=80

        # cell_text=[ [x] for x in point_dataframe_3857["inscription"].values]
        # rowLabels=point_dataframe_3857["EDCS-ID"].values
        # colLabels=["Inscription"]
        # print(rowLabels)
        # print(colLabels)

        # # table = plt.table(cellText = cell_text,
        # #                   rowLabels=rowLabels,
        # #                   colLabels=colLabels)
        # plt.axis('off')
        # plt.grid('off')



        pdf.savefig(fig,dpi=dpi, bbox_inches='tight')
        plt.close()
        print("Saved inscription(s)...")
      #pdf.savefig()


  #plt.savefig(f"{map_filename}.png", dpi=dpi,bbox_inches='tight')
  #subprocess.call(["xdg-open", MAP_FILENAME])


      plt.close()
    print("Done!")

def make_recent_map():

  OUTPUTS = Path("output")

  def get_outputs():
        outputs = {}
        for output in OUTPUTS.glob("*.tsv"):
            outputs[output.stat().st_mtime] = (output.name, output)
        output_keys = sorted(outputs, reverse=True)
        
        filenames = []
        for key in output_keys:
            filenames.append(outputs[key])
        
        
        return filenames
  

  output_tsv = get_outputs()[0][1]
  # print(f"making {output_tsv} png")
  # make_map(data_file=output_tsv,           
  #          show_ids=True,
  #          filetype='png',
  #          append_inscriptions=False,
  #          dpi=300
  #          )
  print(f"making {output_tsv} pdf")
  make_map(data_file=output_tsv,           
           show_ids=False,
           filetype='pdf',
           province_shapefilename="roman_empire_ad_117.shp",
           append_inscriptions=True,
           dpi=300
           )

  #pre_geo_data = {'objects':[], 'geometry':[]}

  # for row in import_rows:
  #   if DEBUG:
  #     print(row)
  # # objects.append(row)
  # # geometry.append(Point())

  # try:
  #   shutil.move("output_maps/*", "old_maps")
  # except:
  #   print("No old maps to move from output_maps to old_maps.")


  # try:
  #   os.mkdir("output_maps")
  # except:
  #   pass

  # try:
  #   os.makedirs("already_mapped_data/output/", exist_ok=True)
  # except FileExistsError:
  #   pass

  # for file in glob.glob(f"{DATA_DIR}/*.tsv"):
  #   print(f"Rendering: {file}")
  #   makeMap(file, map_title_text,roads_3857, provinces_3857, cities_geodataframe_3857, basemap_multicolour=basemap_multicolour, province_shapefilename = province_shapefile)
  #   makeMap(file, map_title_text,roads_3857, provinces_3857, cities_geodataframe_3857, basemap_multicolour=basemap_multicolour, province_shapefilename = province_shapefile, cities=False, roads=False)
    # shutil.move(file, f"already_mapped_data/{file}")

  print("Done Rendering maps.")



if __name__ == "__main__":
  make_recent_map()

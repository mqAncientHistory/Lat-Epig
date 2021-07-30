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
from scalebar import scale_bar

import cartopy.crs as ccrs

# https://github.com/geopandas/geopandas/issues/1597
from matplotlib_scalebar.scalebar import ScaleBar

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


#https://geopython.github.io/OWSLib/#wms
#from owslib.wms import WebMapService
#from owslib.wfs import WebFeatureService

# TO DISABLE SSL CHECKING 
# $ export CURL_CA_BUNDLE=""; ./make_map.py




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
def makeMap(data_file, map_title_text, roads_3857, provinces_3857, cities_geodataframe_3857,  province_shapefilename,searchterm="", provinces=True, roads=True, cities=True):
  point_dataframe_3857 = makeDataframe(data_file)

  #pprint(point_dataframe_3857[["geometry", "Longitude", "Latitude" ]])
  print(f"Making {data_file}\n\troads: {roads}\n\tprovinces: {provinces}\n\tcities: {cities}\n")

  fig = plt.figure()

 
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
  if map_title_text:
    print(f"making map with title {map_title_text}")
  else:
    map_title_text = data_file.replace("-"," ").replace("_"," ").replace(".tsv","")
  
  map_metadata_list=data_file.replace("output/","").replace(".tsv","").split("-")
  search_params = map_metadata_list[3].replace("_"," ").replace("term1","Term 1 =").replace("term2","Term 2 =").replace("%","All").replace("+","; ").replace(r" +"," ")

  map_metadata = f"""Search Parameters: {search_params}
Results: {map_metadata_list[4]} Date scraped: {map_metadata_list[0]}-{map_metadata_list[1]}-{map_metadata_list[2]}
Data from Epigraphik-Datenbank Clauss / Slaby"""
  

  print(f"making map with title {map_title_text}")
  print(f"making map with metadata {map_metadata_list} rendered as \n{map_metadata}")
  plt.tight_layout()
  plt.suptitle(map_metadata, fontsize=6, y=0.10)
  plt.title(map_title_text, fontsize=12, y=1)


  #https://gis.stackexchange.com/a/266833
  buffer = geopandas.GeoDataFrame(geometry=point_dataframe_3857.buffer(MIN_MAP, cap_style = 3))

  xmin, ymin, xmax, ymax = buffer.total_bounds


  #pprint((xmin, ymin, xmax, ymax, buffer.total_bounds, point_dataframe_3857.total_bounds))

  #THIS PROBABLY IS WRONG, BUT IT MAKES A MAP?!
  bounded_prov = geopandas.overlay(buffer, provinces_3857, how='union', keep_geom_type=False)
  province_shapefilename=province_shapefilename.replace("_provinces.shp", "").replace("ad","AD").replace("bc","BC").replace("roman_","").replace("empire_","").replace("_"," ")
  province_shapefilename=f"Provinces in {province_shapefilename}"
  pprint(province_shapefilename)
  if provinces:
    #bounded_prov.plot(ax=ax, linewidth=1, alpha=0.1,  cmap=plt.get_cmap("prism"), zorder=1, label="Provinces")
    bounded_prov.plot(ax=ax, linewidth=0.3, alpha=1, color='#C39B77', linestyle='dashed', zorder=1, label=province_shapefilename)
  if roads:
    bounded_roads = roads_3857.cx[xmin:xmax, ymin:ymax]
    bounded_roads.plot(ax=ax, linewidth=0.2, alpha=1,  color='gray', zorder=2, label="Roads")
  if cities:
    bounded_cities = cities_geodataframe_3857.cx[xmin:xmax, ymin:ymax]
    bounded_cities.plot(ax=ax, marker="+", markersize=3, linewidth=0.25, alpha=0.5,  color='black', zorder=3, label="Cities")
  if searchterm:
    searchterm = f"Inscription:\n{searchterm}"
  else:
    searchterm = "Inscription"
  point_dataframe_3857.plot(ax=ax, marker=".", linewidth=0.2, markersize=5, alpha=0.5, color='red', edgecolor='k', zorder=4, label=f"{searchterm}")
  #ctx.add_basemap(ax, source=ctx.providers.Stamen.TerrainBackground)


  

  ax.legend(fontsize='small')


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

  x, y, arrow_length = 0.025, 0.1, 0.075
  ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
              arrowprops=dict(facecolor='black', arrowstyle='->'),#width=.05, headwidth=2),
              ha='center', va='center', fontsize=5,
              xycoords=ax.transAxes)
  # point_geodataframe.plot(ax=ax, color='red')
  #https://stackoverflow.com/a/53735672

  print("\n\n***\n\nBRIAN", fig.bbox, (bounded_prov.total_bounds[2] - bounded_prov.total_bounds[0]))
  #if (buffer.total_bounds[2] - buffer.total_bounds[0]) < 1000000:
  #  scale = 100
  #else:
  scale = 1_000

  scale_bar(ax, (0.05, 0.05), scale)
  ax.xaxis.set_visible(False)
  ax.set_xticks([0]) 

  ax.autoscale_view(tight=True)

  province_shapefilename=province_shapefilename.replace(" ","_")
  datafile_base_name = data_file.replace("output/","").replace('.tsv','')
  map_filename=f"output_maps/{datafile_base_name}{f'-with{province_shapefilename}' if provinces else ''}{'-withCities' if cities else ''}{'-withRoads' if roads else ''}"
  
  
  ax.spines['geo'].set_visible(False)

  
  #ax.get_tightbbox()
  #ax.outline_patch.set_visible(False)
  plt.savefig(f"{map_filename}.pdf", dpi=1200,bbox_inches='tight')
  plt.savefig(f"{map_filename}.png", dpi=1200,bbox_inches='tight')
  #subprocess.call(["xdg-open", MAP_FILENAME])


  plt.close()

def main(map_title_text, province_shapefile):

  cities_rows = extract(CITIES_DATA)
  cities_dataframe = pandas.DataFrame(cities_rows)


  #https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/

  roads_3857 = geopandas.read_file(ROMAN_ROADS_SHP).to_crs(epsg=3857)
  provinces_3857 = geopandas.read_file(PROVINCES_SHP / province_shapefile).to_crs(epsg=3857)


  cities_geodataframe_3857 = geopandas.GeoDataFrame(
    cities_dataframe,
    geometry=geopandas.points_from_xy(
      cities_dataframe["Longitude (X)"],
      cities_dataframe["Latitude (Y)"]),
    crs="EPSG:4326").to_crs(epsg=3857)

  geopandas.options.use_pygeos = True
  
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

  for file in glob.glob(f"{DATA_DIR}/*.tsv"):
    print(f"Rendering: {file}")
    makeMap(file, map_title_text,roads_3857, provinces_3857, cities_geodataframe_3857, province_shapefilename = province_shapefile)
    makeMap(file, map_title_text,roads_3857, provinces_3857, cities_geodataframe_3857, province_shapefilename = province_shapefile, cities=False, roads=False)
    # shutil.move(file, f"already_mapped_data/{file}")

  print("Done Rendering maps.")

if __name__ == "__main__":
  main(map_title_text=str(datetime.datetime.now()), province_shapefile="roman_empire_60_bc_provinces.shp" )

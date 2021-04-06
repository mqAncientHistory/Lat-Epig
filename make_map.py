#!/usr/bin/env python
# GPL v3 Brian Ballsun-Stanton
# Taken from https://automating-gis-processes.github.io/2016/Lesson5-static-maps.html


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
PROVINCES_SHP   = SUPPORTING_DATA / "cultural_data" / "political_shading" / "roman_empire_ad_117" / "shape" / "roman_empire_ad_117.shp"
#CITIES_SHP      = SUPPORTING_DATA / "strabo_data" / "straborivers_current.shp"
CITIES_DATA     = Path("cities") / "Hanson2016_Cities_OxREP.csv"

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
  print(f"Making {data_filename}\n\troads: {roads}\n\tprovinces: {provinces}\n\tcities: {cities}\n")
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
def makeMap(data_file, roads_3857, provinces_3857, cities_geodataframe_3857, provinces=True, roads=True, cities=True):
  point_dataframe_3857 = makeDataframe(data_file)


  fig, ax = plt.subplots()


  #https://geopandas.org/gallery/plotting_with_geoplot.html
  world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
  # ax = geoplot.polyplot(
  #     world, 
  #     #projection=geoplot.crs.Orthographic(), 
  #     figsize=(8, 4)
  # )

  plt.title(data_filename.replace("-"," ").replace("_"," ").replace(".tsv",""))

  #https://gis.stackexchange.com/a/266833
  xmin, ymin, xmax, ymax = point_geodataframe_3857.total_bounds

  if provinces:
    bounded_prov = provinces_3857.cx[xmin:xmax, ymin:ymax]
    bounded_prov.plot(ax=ax, linewidth=1, alpha=0.1,  cmap=plt.get_cmap("prism"), zorder=1)
  if roads:
    bounded_roads = roads_3857.cx[xmin:xmax, ymin:ymax]
    bounded_roads.plot(ax=ax, linewidth=0.2, alpha=1,  color='gray', zorder=2)
  if cities:
    bounded_cities = cities_geodataframe_3857.cx[xmin:xmax, ymin:ymax]
    bounded_cities.plot(ax=ax, marker="s", markersize=0.1, linewidth=0.25, alpha=0.5,  color='black', zorder=3)
  point_geodataframe_3857.plot(ax=ax, marker="^", linewidth=0.2, markersize=2, alpha=0.5, color='red', edgecolor='k', zorder=4)
  #ctx.add_basemap(ax, source=ctx.providers.Stamen.TerrainBackground)

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

  #point_geodataframe.plot(ax=ax, color='red')
  #https://stackoverflow.com/a/53735672
  map_filename=f"output_maps/{data_filename.replace('.tsv','')}{'-withProvinces' if provinces else ''}{'-withCities' if cities else ''}{'-withRoads' if roads else ''}"
  plt.savefig(f"{map_filename}.pdf", dpi=1200,bbox_inches='tight')
  #plt.savefig(f"{map_filename}.png", dpi=1200,bbox_inches='tight')
  #subprocess.call(["xdg-open", MAP_FILENAME])
  plt.close()

def main():

  cities_rows = extract(CITIES_DATA)
  cities_dataframe = pandas.DataFrame(cities_rows)


  #https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/

  roads_3857 = geopandas.read_file(ROMAN_ROADS_SHP).to_crs(epsg=3857)
  provinces_3857 = geopandas.read_file(PROVINCES_SHP).to_crs(epsg=3857)


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

  try:
    shutil.move("output_maps/*", "old_maps")
  except:
    print("No old maps to move from output_maps to old_maps.")


  try:
    os.mkdir("output_maps")
  except:
    pass

  try:
    os.makedirs("already_mapped_data/output/", exist_ok=True)
  except FileExistsError:
    pass

  for file in glob.glob(f"{DATA_DIR}/*.tsv"):
    print(f"Rendering: {file}")
    makeMap(file, roads_3857, provinces_3857, cities_geodataframe_3857)
    makeMap(file, roads_3857, provinces_3857, cities_geodataframe_3857, cities=False, roads=False)
    shutil.move(file, f"already_mapped_data/{file}")

  print("Done Rendering maps.")

if __name__ == "__main__":
  main()

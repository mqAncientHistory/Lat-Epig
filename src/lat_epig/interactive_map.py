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

import folium
from folium import plugins
import random
import simplejson as json
import textwrap
from yaspin import yaspin


def makeDataframe(data_file, epsg=3857):
    
    # pprint(WMS_LAYERS)
    # pprint([op.name for op in wms.operations])

    # https://frictionlessdata.io/tooling/python/extracting-data/
    # Handles multiline columns cleanly.
    data_filename = os.path.basename(data_file)
    #print(f"Making {data_filename}\n\troads: {roads}\n\tprovinces: {provinces}\n\tcities: {cities}\n")
    import_rows = extract(data_file)
    
    #pprint(import_rows[0])
    import_dataframe = pandas.DataFrame(import_rows)

    #cities_3857 = geopandas.read_file(CITIES_SHP).to_crs(epsg=3857)

    point_geodataframe = geopandas.GeoDataFrame(
    import_dataframe[import_dataframe.Longitude.notnull()],
    geometry=geopandas.points_from_xy(
    import_dataframe[import_dataframe.Longitude.notnull()].Longitude,
    import_dataframe[import_dataframe.Longitude.notnull()].Latitude),
    crs="EPSG:4326")
    point_geodataframe[['Latitude', 'Longitude']] = point_geodataframe[['Latitude', 'Longitude']].apply(pandas.to_numeric)
    
    def linkify(edcs_id):
        myid=edcs_id.replace("EDCS-","")
        return f"""<form name='epi' action='http://db.edcs.eu/epigr/epi_ergebnis.php' method='POST' target="_blank">
          <input type="hidden" name="p_edcs_id" value="{myid}"/>
          <input type="submit" name="cmdsubmit" value="Open in EDCS" >
          </form>
        """

    point_geodataframe['EDCS Link'] = point_geodataframe['EDCS-ID'].apply(linkify)

    point_geodataframe['cleaned inscription'] = point_geodataframe['inscription interpretive cleaning'].apply(lambda x: textwrap.shorten(x or 'null', width=255))
    
    point_geodataframe_3857 = point_geodataframe.to_crs(epsg=epsg)
    return point_geodataframe_3857
    
@yaspin(text="Making interactive maps...")
def make_interactive_map(data_file):
  DATA_DIR = "output"
  SUPPORTING_DATA = Path("awmc.unc.edu")
  SUPPORTING_DATA = SUPPORTING_DATA / "awmc" / "map_data" / "shapefiles"
  ROMAN_ROADS_SHP = SUPPORTING_DATA / "ba_roads" / "ba_roads.shp"
  PROVINCES_SHP   = SUPPORTING_DATA / "cultural_data" / "political_shading" / "roman_empire_ad_117" / "shape" / "roman_empire_ad_117.shp"
  CITIES_DATA     = Path("cities") / "Hanson2016_Cities_OxREP.csv"

  cities_rows = extract(CITIES_DATA)
  cities_dataframe = pandas.DataFrame(cities_rows)


  #https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/

  roads_4326 = geopandas.read_file(ROMAN_ROADS_SHP).to_crs(epsg=4326)
  provinces_4326 = geopandas.read_file(PROVINCES_SHP).to_crs(epsg=4326)


  cities_geodataframe_4326 = geopandas.GeoDataFrame(
  cities_dataframe,
  geometry=geopandas.points_from_xy(
    cities_dataframe["Longitude (X)"],
    cities_dataframe["Latitude (Y)"]),
  crs="EPSG:4326").to_crs(epsg=4326)
  cities_geodataframe_4326.drop("Longitude (X)", inplace=True, axis=1)
  cities_geodataframe_4326.drop("Latitude (Y)", inplace=True, axis=1)

  #pprint(cities_geodataframe_4326)
  geopandas.options.use_pygeos = True



  # TODO https://nbviewer.jupyter.org/github/python-visualization/folium_contrib/blob/master/notebooks/HereMapsApiExplorer_no_creds.ipynb get this out of the display file



  output_maps ={}

  xmin, ymin, xmax, ymax = (0,0,10000,10000)


  #for file in glob.glob(f"{DATA_DIR}/*.tsv"):
  df =  makeDataframe(data_file, epsg=4326)
  #pprint(df)
  map_xmin, map_ymin, map_xmax, map_ymax = df.total_bounds

  xmin = max(xmin, map_xmin)
  ymin = max(ymin, map_ymin)
  xmax = min(xmax, map_xmax)
  ymax = min(ymax, map_ymax)
  
  output_maps[data_file] = df.to_json()



      
  # Create a map using the Map() function and the coordinates for Boulder, CO
  scrape_map = folium.Map(location=[41.9028, 12.4964], 
                          zoom_start=5,
                          
                          #tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
                          #attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                          
                          tiles = 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png',
                          attr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  )

  # Display the map

  #cities = folium.features.GeoJson(cities_geodataframe_4326.to_json()).add_to(scrape_map)
  # Running the above crashes the tab

  # scrape_map.add_child(cities)
  #https://leafletjs.com/reference-1.6.0.html#path-option
  road_style = {'color':'#000000',
                'opacity': 0.5}
  roads = folium.features.GeoJson(roads_4326.to_json(),
                                  name='Roads',
                                  style_function=lambda x: road_style).add_to(scrape_map)


  #https://stackoverflow.com/a/45081821
  r = lambda: (random.randint(0,255))


  for map_json in output_maps:
      # https://github.com/python-visualization/folium/issues/1385
      folium.features.GeoJson(output_maps[map_json],
                              name=f"{map_json}",
                              popup=folium.GeoJsonPopup(["EDCS-ID","EDCS Link","raw dating","province", "place", "Material", "cleaned inscription"])
                             ).add_to(scrape_map)


  def province_style(arg):
      return {
          'weight': 2,
          'opacity': 1,
          'color': '#ffffff',
          'dashArray': 3,
          'fillOpacity': 0.4,
          'fillColor': "#{:02x}{:02x}{:02x}".format(r(), r(), r())
      }
  provinces = folium.features.GeoJson(provinces_4326.to_json(), style_function=province_style).add_to(scrape_map)


  return scrape_map
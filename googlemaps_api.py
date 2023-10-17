#We're calling the Google Geocoding API in order to establish if a station is within the limits of a city or town
import googlemaps 
import requests
import pandas as pd
import json
from urllib.request import urlopen
from dotenv import load_dotenv
import os


load_dotenv()


def coords_dec(latitud, longitud):
    # Transform the coords in a format accepted by the API
    # Return them as a duple

    # First, we extract the values in grades, minutes and seconds
    latitud_grados = float(latitud[:2])
    latitud_minutos = float(latitud[2:4])
    latitud_segundos = float(latitud[4:6])

    longitud_grados = float(longitud[:2])
    longitud_minutos = float(longitud[2:4])
    longitud_segundos = float(longitud[4:6])


    # We transform them to decimal
    latitud_decimal = latitud_grados + (latitud_minutos / 60) + (latitud_segundos / 3600)
    longitud_decimal = longitud_grados + (longitud_minutos / 60) + (longitud_segundos / 3600)

    # And keep the direction 
    if latitud.endswith("S"):
        latitud_decimal *= -1  # South means negative
    if longitud.endswith("W"):
        longitud_decimal *= -1  # West means negative

    return latitud_decimal, longitud_decimal

def get_localidad():
    # We extract the town from the json file
    # The return value is a 'compound_code' with an at least 6 char code that also contains the town and country
    # We clean it in order to keep just the town value

    if len(data_json['plus_code']) == 2:
        
        localidad = data_json['plus_code']['compound_code']
        localidad = localidad.split(",")
        
        localidad = localidad[0].split(" ", 1)
        return localidad[1]
    else:
        return None


# We get the API key and also the origin and destiny's files' paths
# We already extracted the weather stations from the AEMET API and save them to a csv

apikey = os.environ.get('api_key_maps')
csv_origin_path = os.environ.get('csv_origin_path')
csv_end_path = os.environ.get('csv_end_path')
estaciones = pd.read_csv(csv_origin_path, sep=";", on_bad_lines='skip')

loc_estaciones = []

for index2, row2 in estaciones.iterrows():
    # First, we transform the coords
    
    latitud, longitud = coords_dec(row2['latitud'],row2['longitud'])
    
    # Now we create the URL request
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitud) + "," + str(longitud) + "&key=" + apikey
    response = urlopen(url)
    data_json = json.loads(response.read())
    
    # With the station coords, we obtain the town
    localidad = get_localidad()

    loc_estaciones.append([row2['indicativo'], localidad])


if len(loc_estaciones) > 0:
    df_estaciones = pd.DataFrame(loc_estaciones)
    df_estaciones.to_csv(csv_end_path,sep=";")
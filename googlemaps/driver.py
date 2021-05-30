import itertools
from google.cloud import translate_v2 as translate
import os
import googlemaps
from datetime import datetime
from GoogleMapsAPIKey import get_my_key
import time
import pandas as pd
import _pickle as pickle
import json
from text_unidecode import unidecode
# from pydrive.auth import GoogleAuth
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Bachelor\google-maps-services-python\google-maps-services-python-master\googlemaps\igneous-river-310512-373a899234a0.json"

translate_client = translate.Client()

API_KEY = get_my_key()
gmaps = googlemaps.Client(key=API_KEY)


def poi_streets():
    # Load data
    df_street_names = pd.read_csv('D:\Bachelor\Masr_El_Gedida_Data\Masr_El_Gedida_Streets1.csv', usecols=[
        'name', 'highway'])

    # remove null values
    df_street_names = df_street_names[df_street_names['name'].notna()]
    df_street_names = df_street_names.drop_duplicates(
        subset=['name'])  # remove duplicates

    df_street_names = df_street_names.iloc[286:]
    # limit = 1
    # for index, row in itertools.islice(df_street_names.iterrows(), limit):
    for index, row in df_street_names.iterrows():
        dict_sample = []
        curr_st = row['name']
        print(f"STREET NAME {curr_st}")
        places_result = gmaps.places(
            query="points of interest near " + curr_st + " heliopolis"
        )
        result = places_result['results']
        for index in range(len(result)):
            temp_dict = {}
            if 'name' in result[index]:
                temp_dict['name'] = result[index]['name']
            if 'formatted_address' in result[index]:
                temp_dict['formatted_address'] = result[index]['formatted_address']
            if 'geometry' in result[index]:
                if 'location' in result[index]['geometry']:
                    if 'lat' in result[index]['geometry']['location']:
                        temp_dict['lat'] = result[index]['geometry']['location']['lat']
            if 'geometry' in result[index]:
                if 'location' in result[index]['geometry']:
                    if 'lng' in result[index]['geometry']['location']:
                        temp_dict['lat'] = result[index]['geometry']['location']['lng']
            if 'types' in result[index]:
                temp_dict['types'] = result[index]['types']
            if 'place_id' in result[index]:
                temp_dict['place_id'] = result[index]['place_id']

            dict_sample.append(temp_dict)

        while 'next_page_token' in places_result:
            # pause script 2 seconds to allow the token to be validated on Google's servers
            time.sleep(2)
            places_result = gmaps.places(
                query="points of interest near " + curr_st + " Heliopolis",
                page_token=places_result['next_page_token'])
            result = places_result['results']
            for index in range(len(result)):
                temp_dict = {}
                if 'name' in result[index]:
                    temp_dict['name'] = result[index]['name']
                if 'formatted_address' in result[index]:
                    temp_dict['formatted_address'] = result[index]['formatted_address']
                if 'geometry' in result[index]:
                    if 'location' in result[index]['geometry']:
                        if 'lat' in result[index]['geometry']['location']:
                            temp_dict['lat'] = result[index]['geometry']['location']['lat']
                if 'geometry' in result[index]:
                    if 'location' in result[index]['geometry']:
                        if 'lng' in result[index]['geometry']['location']:
                            temp_dict['lat'] = result[index]['geometry']['location']['lng']
                if 'types' in result[index]:
                    temp_dict['types'] = result[index]['types']
                if 'place_id' in result[index]:
                    temp_dict['place_id'] = result[index]['place_id']

                dict_sample.append(temp_dict)

        def reformat_string(x): return unidecode(
            str.lower(x).replace(' ', '_'))

        translated_st_name = translate_client.translate(
            curr_st, target_language="en")
        fileName = reformat_string(translated_st_name['translatedText'])

        with open(f"D:\Bachelor\google-maps-services-python\google-maps-services-python-master\data\{fileName}.json", "a", encoding='utf8') as textfile:
            json_str = json.dumps(dict_sample, ensure_ascii=False)
            textfile.write(json_str)


# Geocoding an address
# bounds = {"northeast": { "lat": 30.013146, "lng": 31.298097},"southwest": {"lat": 30.013963,"lng": 31.285748}}
# geocode_result = gmaps.geocode(address='9, Al-Mokattam St., Al Abageyah, El-Mukkatam, Cairo Governorate, Egypt')  # 30.013071,31.292913


# latlng = {'lat': 30.0129508, 'lng': 31.2929074}
# places_result = gmaps.places_nearby(
#    location=latlng,
#    keyword="store",
#    rank_by="distance",
#    type="وجيا ا",
# )
# length_dict = len(places_result['results'])


# for x in range(length_dict):
#   print("name: " + places_result['results'][x]['name'] +
#        " ,  vicinity: " + places_result['results'][x]['vicinity'])

# pause script 3 seconds
# time.sleep(3)
# get next 20 results
# for x in range(2):
#       places_result = gmaps.places_nearby(
#         page_token=places_result['next_page_token'])
#  for y in range(length_dict):
#     print("name:" + places_result['results'][y]['name'] +
#          " ,  vicinity: " + places_result['results'][y]['vicinity'])
# time.sleep(3)

def reverse_geocode():
    def reformat_string2(x):
        data = x.encode("utf-8")
        data2 = str(x).replace('،', '_')
        data2 = data2.replace(',', '_')
        data3 = data2.encode("utf-8")
        return data3.decode("utf-8")

    # Load data
    df_nodes = pd.read_csv('D:\Bachelor\Masr_El_Gedida_Data\osm_files\masr_el_gedida_nodes.csv', usecols=['id',
                                                                                                          'lon', 'lat'])
    # limit = 1
    # for index, row in itertools.islice(df_nodes.iterrows(), limit):
    total_address = []
    for index, row in df_nodes.iterrows():
        lat = row['lat']
        lng = row['lon']
        address = ""
        reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
        for i in range(4):
            address = address + " || " + \
                reformat_string2(
                    reverse_geocode_result[i]['formatted_address'])
        total_address.append(address)
    df_nodes['Address'] = total_address
    df_nodes.to_csv(r"D:\Bachelor\google-maps-services-python\google-maps-services-python-master\data\Nodes\masr_el_gedida_nodes.csv",
                    index=False, encoding='utf-8')
    print(total_address)


reverse_geocode()


# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((30.0982001, 31.3273624))
# AWEL ENTRY FEL EGDES CSV FILE


# 30.090451899999998, 31.3140552 7 Abd Allah Nour, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt
# 30.0901738,31.3139689 7 Abd Allah Nour, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt


# TANY ENTRY FEL EDGES CSV FILE
# 30.0901738,31.3139689 7 Abd Allah Nour, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt
# 30.0899713,31.313744 6 Abd Allah Nour, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt

# TALET
# 30.0899713,31.313744 6 Abd Allah Nour, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt
# 30.0895944, 31.3133254 8 Abou Al Mahasen, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt

# RAQAM 2039
# 30.0895944, 31.3133254 8 Abou Al Mahasen, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt
# 30.089749899999997,31.3131347 8 Abou Al Mahasen, Mansheya El-Bakry, Heliopolis, Cairo Governorate, Egypt

# print(reverse_geocode_result[0]['formatted_address'])
# Request directions via public transit
# now = datetime.now()

# directions_result = gmaps.directions("place_id:ChIJfRkYns44WBQR_gcQa-qohUs","place_id:ChIJLwGfx8k4WBQRevJnI1s5cdc",mode="walking",alternatives=True,departure_time=now)

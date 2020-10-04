import requests
import pandas as pd
from decouple import config


def bike_station_dataframe():
    BIKE_API_KEY = config('BIKE_API_KEY')
    payload = {
        'key': BIKE_API_KEY, 'schemeId': '3'}
    r = requests.post(
        "https://data.bikeshare.ie/dataapi/resources/station/data/list", data=payload)
    full_dict = r.json()
    bike_json = full_dict['data']
    bike_df = pd.DataFrame(bike_json)
    bike_df.to_csv('../limk-data/LimerickBikeStations.txt', index=False)


bike_station_dataframe()

import pandas as pd
import requests
import json
from decouple import config


def inner_json_to_pandas(dataframe, string):
    target_df = pd.read_json((dataframe[string]).to_json(), orient='index')
    target_df = target_df.sort_index(axis=0)
    return target_df


def prepend_identifier(dataframe, string):
    return [string + row for row in dataframe]


def parse_time_format(s):
    """Parse all occurences of - to / for correct time formatting."""
    s = s.replace("-", "/")
    s = s.replace("T", " ")
    sep = '+'
    rest = s.split(sep, 1)[0]
    return rest


def airport_schedule_dataframe(flight_type_iata, flight_type_schedule):
    """Expects either "dep_iata" with "departure_scheduled"
    or "arr_iata" with "arrival_scheduled"."""
    # departure information for shannon
    AVI_API_KEY = config('AVI_API_KEY')
    payload = {'access_key': AVI_API_KEY,
               flight_type_iata: 'SNN'}
    r = requests.get('http://api.aviationstack.com/v1/flights', params=payload)
    # parse to json dtype
    full_dict = r.json()
    # target required information
    schedule_json = full_dict['data']
    # create pandas df from json
    schedule_df = pd.DataFrame(schedule_json)
    flight_status_df = schedule_df[['flight_status']]
    df_departure = inner_json_to_pandas(schedule_df, "departure")
    df_arrival = inner_json_to_pandas(schedule_df, "arrival")
    df_airline = inner_json_to_pandas(schedule_df, "airline")
    df_flight = inner_json_to_pandas(schedule_df, "flight")
    df_departure.columns = prepend_identifier(df_departure, "departure_")
    df_arrival.columns = prepend_identifier(df_arrival, "arrival_")
    df_airline.columns = prepend_identifier(df_airline, "airline_")
    df_flight.columns = prepend_identifier(df_flight, "flight_")
    df = df_airline.join(df_flight)
    df = df.join(df_departure)
    df = df.join(df_arrival)
    df = df.join(flight_status_df)
    # organising the rows according to datetime
    df[flight_type_schedule] = pd.to_datetime(df[flight_type_schedule])
    df = df.sort_values(by=flight_type_schedule)
    # reconverting to string value
    df[flight_type_schedule] = df[flight_type_schedule].astype(str)
    df = df[['airline_name', 'flight_iata', 'flight_status', 'departure_airport',
             'departure_scheduled', 'arrival_airport', 'arrival_scheduled']].copy()
    df['departure_scheduled'] = df['departure_scheduled'].apply(
        parse_time_format)
    df['arrival_scheduled'] = df['arrival_scheduled'].apply(parse_time_format)
    return df


departure_schedule_df = airport_schedule_dataframe(
    "dep_iata", "departure_scheduled")
arrival_schedule_df = airport_schedule_dataframe(
    "arr_iata", "arrival_scheduled")


# Write the cleaned dataframes to csv files
departure_schedule_df.to_csv(
    'ShannonDepartureSchedule.txt', index=False)
arrival_schedule_df.to_csv(
    'ShannonArrivalSchedule.txt', index=False)

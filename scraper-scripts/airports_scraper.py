import pandas as pd
import requests
import json
from decouple import config
from utils import inner_json_to_pandas, prepend_identifier, parse_time_format


# expects either "dep_iata" with "departure_scheduled"
# or "arr_iata" with "arrival_scheduled"
def airport_schedule_dataframe(flight_type_iata, flight_type_schedule, airport_iata):
    AVI_API_KEY = config('AVI_API_KEY')
    payload = {'access_key': AVI_API_KEY,
               flight_type_iata: airport_iata}
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


def airports_schedule_csv(airport_list):
    departure_schedule_df_list = []
    arrival_schedule_df_list = []
    for i in airport_list:
        departure_schedule_df = airport_schedule_dataframe(
            "dep_iata", "departure_scheduled", i)
        departure_schedule_df_list.append(departure_schedule_df)
        arrival_schedule_df = airport_schedule_dataframe(
            "arr_iata", "arrival_scheduled", i)
        arrival_schedule_df_list.append(arrival_schedule_df)
    full_departure_df = pd.concat(departure_schedule_df_list)
    full_arrival_df = pd.concat(arrival_schedule_df_list)
    # local machine settings
    # full_departure_df.to_csv(
    #     '../react-flask-app/api/csv_data/AirportsDepartureSchedule.txt', index=False)
    # full_arrival_df.to_csv(
    #     '../react-flask-app/api/csv_data/AirportsArrivalSchedule.txt', index=False)
    # server settings
    full_departure_df.to_csv(
        '/home/ubuntu/LimerickTransport/react-flask-app/api/csv_data/AirportsDepartureSchedule.txt', index=False)
    full_arrival_df.to_csv(
        '/home/ubuntu/LimerickTransport/react-flask-app/api/csv_data/AirportsArrivalSchedule.txt', index=False)


# write to a csv the schedule information for the chosen airports
airports_schedule_csv(["SNN", "ORK", "KIR"])

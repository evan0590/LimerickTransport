import calendar
import json
import requests
import xmltodict
import psycopg2
import pandas as pd
from decouple import config
from datetime import date, datetime


# get the GTFS timetable information
timetable_df = pd.read_csv("google_transit_combined/parsed_stop_times.txt")
# get the GTFS trips information
trips_df = pd.read_csv("google_transit_combined/trips.txt")
# get the GTFS route information
route_df = pd.read_csv("google_transit_combined/routes.txt")
# get the GTFS calendar information
calendar_df = pd.read_csv("google_transit_combined/calendar.txt")
# placeholder object to return to the frontend in the event that no data exists
placeholder = {'results': [
    {
        "idA": "01/01/2020 00:00:00",
        "idB": "",
        "targetA": "",
        "targetB": "",
        "targetC": "",
    },
]}


def parse_midnight(s):
    """Parse all times beginning with 24 to 00.

    A helper function for problematic GTFS_timetable entries."""
    if s[0:2] == "24":
        return "00:" + s[3:]
    else:
        return s


def gtfs_data(stop_id):
    """Returns to the frontend the GTFS timetable information for the requested station.
    GTFS datasets are loaded into pandas dataframes and parsed according to day, time and location.
    Is triggered when no RTPI data exists for the requested station.

    Receives from frontend the users chosen station."""
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()].lower()
    current_date = datetime.now().strftime('%d/%m/%Y ')
    current_time = datetime.now().strftime('%H:%M:%S')
    time_object = datetime.strptime(current_time, '%H:%M:%S').time()
    service_ids_from_calendar_df = calendar_df.loc[calendar_df[day] == 1]
    list_of_service_ids = service_ids_from_calendar_df['service_id'].to_list()
    stop_id_timetable_df = timetable_df.loc[timetable_df['stop_id'] == stop_id]
    list_of_trips = stop_id_timetable_df['trip_id'].to_list()
    trips_df_with_select_trip_ids = trips_df[trips_df['trip_id'].isin(
        list_of_trips)]
    trips_df_with_select_trip_ids_and_service_ids = trips_df_with_select_trip_ids[
        trips_df_with_select_trip_ids['service_id'].isin(list_of_service_ids)]
    list_of_route_ids = trips_df_with_select_trip_ids_and_service_ids['route_id'].to_list(
    )
    route_df_with_select_route_ids = route_df[route_df['route_id'].isin(
        list_of_route_ids)]
    merged_route_and_trips_df = trips_df_with_select_trip_ids_and_service_ids.merge(
        route_df_with_select_route_ids, on="route_id", how='inner')
    merged_df = stop_id_timetable_df.merge(
        merged_route_and_trips_df, on="trip_id", how='inner')
    sub_final_df = merged_df.drop_duplicates(
        subset='arrival_time', keep="first").copy()
    sub_final_df['arrival_time'] = sub_final_df['arrival_time'].apply(
        parse_midnight)
    sub_final_df['trip_headsign'] = sub_final_df['trip_headsign'].str.split(
        '-').str[1]
    final_df = sub_final_df[['arrival_time',
                             'route_short_name', 'trip_headsign']].copy()
    final_df.iloc[:, 0] = current_date + final_df.iloc[:, 0]
    final_df.rename(columns={'arrival_time': 'idA',
                             'route_short_name': 'idB', 'trip_headsign': 'targetA'}, inplace=True)
    arrivaltime = sub_final_df["arrival_time"]
    final_df = final_df.join(arrivaltime)
    final_df['arrival_time'] = pd.to_datetime(
        final_df['arrival_time'], format='%H:%M:%S').dt.time
    final_df = final_df.sort_values(by='arrival_time')
    final_df.rename(columns={'arrival_time': 'targetB'},
                    inplace=True)
    if final_df.empty:
        # no information returned from GTFS dataset
        # return placeholder object to avoid error
        return placeholder
    elif len(final_df.index) > 10:
        # where the dataframe is larger than 10
        # return only the timetable information that occurs after the current time.
        df = final_df[final_df['targetB'] > time_object]
        if df.empty:
            # no information returned from GTFS dataset within the selected timeframe.
            # return placeholder object to avoid error
            return placeholder
        else:
            df = df.sort_values(by='targetB')
            df = df.head(10)
            result = df.to_json(orient="records")
            parsed = json.loads(result)
            return {'results': parsed}
    else:
        df = final_df
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return {'results': parsed}


def rail_data(station_code):
    """Returns to the frontend the real time information for the requested rail station.
    Pandas dataframes used to parse the required data, which is returned to frontend as JSON.

    Receives from frontend the users chosen station."""
    current_date = datetime.now().strftime('%d/%m/%Y ')
    station_url = "http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=" + station_code
    response = requests.get(station_url)
    getStationDataXML = json.dumps(xmltodict.parse(response.text))
    getStationDataXML_json = json.loads(getStationDataXML)
    if len(getStationDataXML_json["ArrayOfObjStationData"]) < 4:
        # no information returned from rail api
        # return placeholder object to avoid error
        return placeholder
    else:
        station_data_json = getStationDataXML_json["ArrayOfObjStationData"]["objStationData"]
        if type(station_data_json) is dict:
            station_data_json = [
                getStationDataXML_json["ArrayOfObjStationData"]["objStationData"]]
        station_data_df = pd.DataFrame(station_data_json)
        final_df = station_data_df[['Origintime', 'Destination']].copy()
        final_df["Line"] = station_data_df.Origin + \
            " " + station_data_df.Direction
        final_df.rename(columns={'Origintime': 'idA',
                                 'Line': 'idB',
                                 'Destination': 'targetA'},
                        inplace=True)
        final_df.idA = current_date + final_df.idA
        arrival_time = station_data_df["Duein"]
        final_df = final_df.join(arrival_time)
        final_df.rename(columns={'Duein': 'targetB'},
                        inplace=True)
        final_df.targetB = final_df["targetB"].astype(int)
        final_df = final_df.sort_values(by='targetB')
        final_df.targetB = final_df["targetB"].astype(str)
        df = final_df
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return {'results': parsed}


def parse_time_format(s):
    """Parse all occurrences of - to / for correct time formatting."""
    s = s.replace("-", "/")
    s = s.replace("T", " ")
    sep = '+'
    rest = s.split(sep, 1)[0]
    return rest


def bike_data(station_id):
    """Returns to the frontend the bike occupancy information for the requested station.
    Occupancy information is taken from a csv file that is updated every 20 mins.
    Pandas dataframes used to parse the required data, which is returned to frontend as JSON.

    Receives from frontend the users chosen station."""
    DB_HOST = config('DB_HOST')
    DB_DATABASE = config('DB_DATABASE')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    conn = psycopg2.connect(database=DB_DATABASE,
                            host=DB_HOST,
                            port=5432, user=DB_USER, password=DB_PASSWORD)
    sql = "SELECT date_status, station_id, docks_available, bikes_available FROM live_bike_data WHERE station_id = " + \
        str(station_id) + " ORDER BY dt DESC LIMIT 1;"
    parsed = []
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        records = cur.fetchall()
        print("Print each row and it's columns values")
        for row in records:
            json_object = {}
            json_object['idA'] = row[0]
            json_object['idB'] = row[1]
            json_object['targetA'] = row[2]
            json_object['targetB'] = row[3]
            parsed.append(json_object)
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return {'results': parsed}


def airport_data(airport, arrival_flag):
    """Returns to the frontend the airport departure information for the requested airport.
    Information is taken from a csv file that is updated every 20 mins.
    Pandas dataframes used to parse the required data, which is returned to frontend as JSON.

    Receives from frontend the users chosen airport."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    airport_iata = "DUB/" if airport == "Dublin" else "SNN/" if airport == "Shannon" else "ORK/"
    dep_or_arr = "departures/" if arrival_flag == "false" else "arrivals/"
    airport_url = "http://ec2-52-19-19-167.eu-west-1.compute.amazonaws.com/" + \
        dep_or_arr + "airportdate/" + airport_iata + current_date
    pop_scheduled = "arrivalScheduled" if arrival_flag == "false" else "departureScheduled"
    target_scheduled = "departureScheduled" if arrival_flag == "false" else "arrivalScheduled"
    target_airport = "arrivalAirport" if arrival_flag == "false" else "departureAirport"
    response = requests.get(airport_url)
    data = response.text
    parsed = json.loads(data)
    for json_object in parsed:
        json_object.pop(pop_scheduled)
        json_object.pop('airport')
        json_object.pop('flightDate')
        json_object['idA'] = json_object.pop(target_scheduled)
        json_object['idB'] = json_object.pop('flightIata')
        json_object['targetA'] = json_object.pop(target_airport)
        json_object['targetB'] = json_object.pop('airlineName')
        json_object['targetC'] = json_object.pop('airportIata')
    return {'results': parsed}

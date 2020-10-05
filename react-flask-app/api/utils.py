import calendar
import pandas as pd
import warnings
import json
from datetime import date, datetime
import requests
import xmltodict

warnings.filterwarnings('ignore')


# get the GTFS timetable information
timetable_df = pd.read_csv(".../google_transit_combined/stop_times.txt")
# get the GTFS trips information
trips_df = pd.read_csv(".../google_transit_combined/trips.txt")
# get the GTFS route information
route_df = pd.read_csv(".../google_transit_combined/routes.txt")
# get the GTFS calendar information
calendar_df = pd.read_csv(".../google_transit_combined/calendar.txt")
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


def rtpi_data(stop_number, nta_api):
    """Returns to the frontend the real time passenger information data for the requested stop.
    Pandas dataframes used to parse the required data, which is returned to frontend as JSON.

    Receives from frontend the users chosen station."""
    url = "https://api.nationaltransport.ie/rtpi/RealTimeBusInformation?stopid=" + \
        stop_number + "&operator=be"
    headers = {'Ocp-Apim-Subscription-Key': nta_api}
    r = requests.get(url, headers=headers)
    full_dict = r.json()
    if next(iter(full_dict.values())) == 429:
        # an overuse block is placed on RTPI API
        # return empty dictionary to trigger call to GTFS dataset.
        results_dict = {}
        return results_dict
    elif full_dict['statusCode'] == 401:
        print("rtpi is now closed")
        results_dict = {}
        return results_dict
    elif full_dict['results'] == []:
        print("hello, im r", r)
        # no information was returned from RTPI API
        # return empty array to trigger call to GTFS dataset.
        return full_dict['results']
    else:
        # information returned, parse to pandas df and return as JSON.
        results_dict = full_dict['results']
        results_df = pd.DataFrame(results_dict)
        df = results_df[['arrivaldatetime',
                         'route', 'destination', 'duetime']].copy()
        df.rename(columns={'arrivaldatetime': 'idA',
                           'route': 'idB',
                           'destination': 'targetA', 'duetime': 'targetB'},
                  inplace=True)
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return {'results': parsed}


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
        subset='arrival_time', keep="first")
    sub_final_df['arrival_time'] = sub_final_df['arrival_time'].apply(
        parse_midnight)
    sub_final_df.trip_headsign = sub_final_df.trip_headsign.str.split(
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
    """Parse all occurences of - to / for correct time formatting."""
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
    bike_df = pd.read_csv(".../limk-data/LimerickBikeStations.txt")
    bike_df['dateStatus'] = bike_df['dateStatus'].apply(parse_time_format)
    df = bike_df.loc[bike_df['stationId'] == int(station_id)]
    df.stationId = df.stationId.astype("str")
    df.docksAvailable = df.docksAvailable.astype("str")
    df.bikesAvailable = df.bikesAvailable.astype("str")
    final_df = df[['dateStatus', 'stationId',
                   'docksAvailable', 'bikesAvailable']].copy()
    final_df.rename(columns={'dateStatus': 'idA',
                             'stationId': 'idB',
                             'docksAvailable': 'targetA',
                             'bikesAvailable': 'targetB'},
                    inplace=True)
    result = final_df.to_json(orient="records")
    parsed = json.loads(result)
    return {'results': parsed}


def airport_data(airport, arrival_flag):
    """Returns to the frontend the airport departure information for the requested airport.
    Information is taken from a csv file that is updated every 20 mins.
    Pandas dataframes used to parse the required data, which is returned to frontend as JSON.

    Receives from frontend the users chosen airport.
    Is currently hardcoded to Shannon Airport only."""
    if arrival_flag == "false":
        df = pd.read_csv(".../limk-data/AirportsDepartureSchedule.txt")
        df = df.loc[df['departure_airport'] == airport].copy()
        df.rename(columns={'departure_scheduled': 'idA',
                           'flight_iata': 'idB',
                           'arrival_airport': 'targetA',
                           'airline_name': 'targetB',
                           'flight_status': 'targetC'},
                  inplace=True)
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return {'results': parsed}
    else:
        df = pd.read_csv(".../limk-data/AirportsArrivalSchedule.txt")
        df = df.loc[df['arrival_airport'] == airport].copy()
        df.rename(columns={'departure_scheduled': 'idA',
                           'flight_iata': 'idB',
                           'arrival_airport': 'targetA',
                           'airline_name': 'targetB',
                           'flight_status': 'targetC'},
                  inplace=True)
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return {'results': parsed}

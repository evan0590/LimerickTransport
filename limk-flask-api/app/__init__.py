# app/__init__.py
from flask import Flask, request
from .utils import rtpi_data, rail_data, gtfs_data, bike_data, airport_data
# from dotenv import load_dotenv

# # the path to your .env file (or any other file of environment variables you want to load)
# load_dotenv('.env')


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    @app.route('/')
    def index():  # pylint: disable=unused-variable
        return f'API_KEY = { app.config.get("API_KEY") }'

    @app.route('/location_info', methods=['POST', 'GET'])
    def location_info():  # pylint: disable=unused-variable
        location_number = request.args.get('locationNumber')
        location_id = request.args.get('locationId')
        location_type = request.args.get('locationType')
        arrival_flag = request.args.get('airportArrivalFlag')
        # print("hello", arrival_flag, type(arrival_flag))
        nta_api = app.config.get("NTA_API_KEY")
        if location_type == "Bus":
            result = rtpi_data(location_number, nta_api)
            if len(result) is 0:
                result = gtfs_data(location_id)
                return result
            else:
                ("Triggered: bus else clause.")
                return result
        elif location_type == "Rail":
            result = rail_data(location_id)
            return result
        elif location_type == "Bike":
            result = bike_data(location_id)
            return result
        elif location_type == "Airport":
            result = airport_data(location_id, arrival_flag)
            return result

    return app

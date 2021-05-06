import time

from dotenv import load_dotenv
from flask import Flask, request

from utils import rail_data, gtfs_data, bike_data, airport_data


def create_app(test_config=None):
    """Create an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/api/location_info', methods=['POST', 'GET'])
    def location_info():  # pylint: disable=unused-variable
        """Serve JSON response from each of the transport types."""
        location_id = request.args.get('locationId')
        location_type = request.args.get('locationType')
        arrival_flag = request.args.get('airportArrivalFlag')
        if location_type == "Bus":
            result = gtfs_data(location_id)
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
        else:
            return {"results": []}

    return app

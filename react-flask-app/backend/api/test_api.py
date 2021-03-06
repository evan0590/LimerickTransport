import os
import sys

import pytest

from flask import json

from api import create_app


@pytest.fixture
def client():
    """Create a new app instance for each test."""
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get('/api/location_info')
    assert response.status_code == 200


def test_bus_route(client):
    """Test the bus route response."""
    bus_route = "/api/location_info?locationNumber=608341&locationId=8400B6083401&locationType=Bus&airportArrivalFlag=false"
    response = client.get(bus_route)

    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(json_data['results']) > 0


def test_rail_route(client):
    """Test the rail route response."""
    rail_route = "/api/location_info?locationNumber=40&locationId=LMRCK&locationType=Rail&airportArrivalFlag=false"
    response = client.get(rail_route)

    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(json_data['results']) > 0


def test_bike_route(client):
    """Test the bike route response."""
    bike_route = "/api/location_info?locationNumber=3010&locationId=3010&locationType=Bike&airportArrivalFlag=false"
    response = client.get(bike_route)

    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(json_data['results']) > 0


def test_air_route(client):
    """The the airport route response."""
    air_route = "/api/location_info?locationNumber=6296700&locationId=Shannon&locationType=Airport&airportArrivalFlag=false"
    response = client.get(air_route)

    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(json_data['results']) >= 0

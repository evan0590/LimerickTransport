import os
import sys

import pytest

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
    bus_route = "/api/location_info?locationNumber=608341&locationId=8400B6083401&locationType=Bus&airportArrivalFlag=false"
    response = client.get(bus_route)
    assert response.status_code == 200


def test_rail_route(client):
    rail_route = "/api/location_info?locationNumber=40&locationId=LMRCK&locationType=Rail&airportArrivalFlag=false"
    response = client.get(rail_route)
    assert response.status_code == 200


def test_bike_route(client):
    bike_route = "/api/location_info?locationNumber=3010&locationId=3010&locationType=Bike&airportArrivalFlag=false"
    response = client.get(bike_route)
    assert response.status_code == 200


def test_air_route(client):
    air_route = "/api/location_info?locationNumber=6296700&locationId=Shannon&locationType=Airport&airportArrivalFlag=false"
    response = client.get(air_route)
    assert response.status_code == 200

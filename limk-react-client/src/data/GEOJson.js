// Importing the Dublin Bus API stops data
const busData = require("./MidWestBusStops.json");
const railData = require("./MidWestRailStations.json");
const bikeData = require("./LimerickBikeStations.json");
const airData = require("./IrishAirports.json");

// Parsing the Stops data into various object shapes.
const BusGEOJson = busData.map((stop) => ({
  description: stop.stop_name,
  type: "Bus",
  // icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  icon: {
    url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
    scaledSize: { width: 25, height: 25 },
  },
  properties: {
    id: stop.stop_id,
    number: stop.stop_name.substr(stop.stop_name.length - 6),
  },
  geometry: {
    type: "Point",
    pos: {
      lat: parseFloat(stop.stop_lat),
      lng: parseFloat(stop.stop_lon),
    },
  },
}));

const RailGeoJson = railData.map((station) => ({
  description: station.StationDesc,
  type: "Rail",
  icon: {
    url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
  },
  properties: {
    id: station.StationCode,
    number: parseInt(station.StationId),
  },
  geometry: {
    type: "Point",
    pos: {
      lat: parseFloat(station.StationLatitude),
      lng: parseFloat(station.StationLongitude),
    },
  },
}));

const BikeGeoJson = bikeData.map((bike) => ({
  description: bike.name,
  type: "Bike",
  icon: {
    url: "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
    scaledSize: { width: 35, height: 35 },
  },
  properties: {
    id: bike.stationId,
    number: parseInt(bike.stationId),
  },
  geometry: {
    type: "Point",
    pos: {
      lat: parseFloat(bike.latitude),
      lng: parseFloat(bike.longitude),
    },
  },
}));

const AirGeoJson = airData.map((airport) => ({
  description: airport.airport_name + " Airport",
  type: "Airport",
  icon: {
    url: "http://maps.google.com/mapfiles/ms/icons/purple-dot.png",
    scaledSize: { width: 30, height: 30 },
  },
  properties: {
    id: airport.airport_name,
    number: parseInt(airport.geoname_id),
  },
  geometry: {
    type: "Point",
    pos: {
      lat: parseFloat(airport.latitude),
      lng: parseFloat(airport.longitude),
    },
  },
}));

// GEOJson.push(RailGeoJson);
const GEOJson = BusGEOJson.concat(RailGeoJson, BikeGeoJson, AirGeoJson);

export default GEOJson;

import React, { useState } from "react";
import {
  useLoadScript,
  GoogleMap,
  Marker,
  InfoWindow,
} from "@react-google-maps/api";
import LocationInformation from "./LocationInformation";

// Latitude and longitude coordinates are: 52.668018, -8.630498.
const limerickCenter = require("../data/LimerickCenter.json");
// Importing custom styles to customize the style of Google Map...
// important for including and excluding certain place markers etc.
const normalModeBasic = require("../data/NormalModeBasic");
const mapContainerStyle = {
  height: "93vh",
};

const stopsModule = require("../data/GEOJson");
const stops = stopsModule.default;

export default function Map(props) {
  // carried from Practicum
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_API,
  });
  const center = limerickCenter;
  const [mapOptions, setMapOptions] = useState({
    // gestureHandling: "none",
    styles: normalModeBasic,
    disableDefaultUI: true,
    zoomControl: true,
    maxZoom: 18,
    minZoom: 8,
  });
  // eslint-disable-next-line
  const [zoom, setZoom] = useState(13); // removing unwanted warning.
  // The general things we need to track in state:
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [markerMap, setMarkerMap] = useState({});
  const [infoOpen, setInfoOpen] = useState(false);
  const [geoMarkers, setGeoMarkers] = useState([]);
  const [selected, setSelected] = useState(null); // removing unwanted warning.
  // maintaining state of the airportArrival/Departure
  const [airportDepartureFlag, setAirportDepartureFlag] = useState(true);
  const [airportArrivalFlag, setAirportArrivalFlag] = useState(false);

  const mapRef = React.useRef();
  const onMapLoad = React.useCallback((map) => {
    mapRef.current = map;
  }, []);

  // Orient the map to selected location.
  const panTo = React.useCallback(({ lat, lng }) => {
    mapRef.current.setZoom(16);
    mapRef.current.panTo({ lat, lng });

    setGeoMarkers((current) => [...current, { lat: lat, lng: lng }]);
  }, []);

  const markerLoadHandler = (marker, stop) => {
    return setMarkerMap((prevState) => {
      return { ...prevState, [stop.properties.id]: marker };
    });
  };

  const markerClickHandler = (event, place) => {
    // Remember which stop was clicked
    setSelectedPlace(place);
    // Required so clicking a 2nd marker works as expected
    if (infoOpen) {
      setInfoOpen(false);
    }
    setInfoOpen(true);
  };

  if (loadError) return "Error";
  if (!isLoaded)
    return (
      <div
        style={{
          position: "fixed",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
        }}
      >
        <p>... loading</p>
      </div>
    );
  return (
    <GoogleMap
      // Inbuilt props: https://react-google-maps-api-docs.netlify.app/#googlemap.
      mapContainerStyle={mapContainerStyle}
      center={center}
      zoom={zoom}
      options={mapOptions}
      onLoad={onMapLoad}
    >
      {stops.map((stop) => (
        <Marker
          icon={stop.icon}
          key={stop.properties.id}
          position={stop.geometry.pos}
          onLoad={(marker) => {
            markerLoadHandler(marker, stop);
            // Changing the bounds to fit map to chosen route's markers.
            // mapRef.current.fitBounds(bounds);
            mapRef.current.setZoom(13);
          }}
          onClick={(event) => {
            markerClickHandler(event, stop);
            props.setLat(stop.geometry.pos.lat);
            props.setLng(stop.geometry.pos.lng);
          }}
          animation={window.google.maps.Animation.DROP}
        />
      ))}
      {infoOpen && selectedPlace && (
        <InfoWindow
          // Inbuilt props: https://react-google-maps-api-docs.netlify.app/#infowindow.
          anchor={markerMap[selectedPlace.properties.id]}
          // onClick={() => {
          //   props.setLat(selectedPlace.geometry.pos.lat);
          //   props.setLng(selectedPlace.geometry.pos.lng);
          // }}
          onCloseClick={() => setInfoOpen(false)}
        >
          <div
            style={{
              textAlign: "center",
              verticalAlign: "middle",
            }}
          >
            <h2>{selectedPlace.description}</h2>
            {/* {console.log(selectedPlace.properties.id)} */}
            <LocationInformation
              number={selectedPlace.properties.number}
              id={selectedPlace.properties.id}
              type={selectedPlace.type}
              airportDepartureFlag={airportDepartureFlag}
              airportArrivalFlag={airportArrivalFlag}
              setAirportDepartureFlag={setAirportDepartureFlag}
              setAirportArrivalFlag={setAirportArrivalFlag}
            ></LocationInformation>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}

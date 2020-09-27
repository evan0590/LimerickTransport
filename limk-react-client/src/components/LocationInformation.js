// Importing outside developed components.
import React from "react";
import { withStyles, makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";
// Promise based HTTP client - https://github.com/axios/axios.
const axios = require("axios");

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

const useStyles = makeStyles({
  table: {
    maxWidth: 600,
    // maxHeight: 500,
  },
});

// Makes GET request to Flask API with user selected location data as parameters.
// Flask makes GET request to the relevant API, which React returns as a Table.
// Clicking a bus stop's marker will display this Table.
const LocationInformation = (props) => {
  const classes = useStyles();
  // A placeholder variable used while waiting for RTPI response.
  const placeholder = {
    results: [
      {
        // date time object
        idA: "01/01/2020 00:00:00",
        // route/stationId
        idB: "",
        // destination/available bikes
        targetA: "",
        // duetime/available bike stations
        targetB: "",
        // airport only
        targetC: "",
      },
    ],
  };
  // The response from the backend we need to track in state:
  const [rawStopData, setRawStopData] = React.useState(placeholder);

  // The Effect Hook used to perform side effects in this component.
  // https://reactjs.org/docs/hooks-effect.html.
  React.useEffect(
    () => {
      const CancelToken = axios.CancelToken;
      const source = CancelToken.source();
      const loadData = () => {
        try {
          axios
            .get(`/location_info`, {
              params: {
                locationNumber: props.number,
                locationId: props.id,
                locationType: props.type,
                airportArrivalFlag: props.airportArrivalFlag,
              },
            })
            .then((res) => {
              setRawStopData(res.data);
            });
        } catch (error) {
          if (axios.isCancel(error)) {
          } else {
            throw error;
          }
        }
      };
      loadData();
      return () => {
        source.cancel();
      };
    },
    // eslint-disable-next-line
    [props]
  ); // react-hooks/exhaustive-deps

  const stopData = rawStopData.results;
  const realInfo = stopData.map((info) => ({
    // date time object
    idA: info.idA,
    // route/stationId
    idB: info.idB,
    // destination/available bikes
    targetA: info.targetA,
    // duetime/available bike stations
    targetB: info.targetB,
    // airport only variable
    targetC: info.targetC,
  }));

  console.log(realInfo);

  if (String(realInfo[0].idA) === "01/01/2020 00:00:00") {
    // Return nothing when the placeholder has been returned.
    return null;
  } else if (String(props.type) === "Bus" || String(props.type) === "Rail") {
    // Tabular information for bus and rail stations.
    return (
      <TableContainer
        component={Paper}
        style={{ maxHeight: "15vh", overflowY: "scroll" }}
      >
        <Table
          className={classes.table}
          size="small"
          aria-label="a dense table"
        >
          <TableHead>
            <TableRow>
              <StyledTableCell>Route</StyledTableCell>
              <StyledTableCell align="center">Destination</StyledTableCell>
              <StyledTableCell align="center">Due</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {realInfo.map((info) => {
              if (info.targetB === "Due")
                // Avoid displaying "Due mins"
                return (
                  <StyledTableRow key={info.idA + info.idB}>
                    <StyledTableCell component="th" scope="row">
                      {info.idB}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetA}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetB}
                    </StyledTableCell>
                  </StyledTableRow>
                );
              else if (info.targetB.includes(":")) {
                // Returns a clock time estimate of bus/train arrival.
                return (
                  <StyledTableRow key={info.idA + info.idB}>
                    <StyledTableCell component="th" scope="row">
                      {info.idB}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetA}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetB}
                    </StyledTableCell>
                  </StyledTableRow>
                );
              } else {
                // Return a time in mins when bus/train is due.
                return (
                  <StyledTableRow key={info.idA + info.idB}>
                    <StyledTableCell component="th" scope="row">
                      {info.idB}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetA}
                    </StyledTableCell>
                    <StyledTableCell align="center">
                      {info.targetB} mins
                    </StyledTableCell>
                  </StyledTableRow>
                );
              }
            })}
          </TableBody>
        </Table>
      </TableContainer>
    );
  } else if (String(props.type) === "Bike") {
    // Tabular information for bike locations
    return (
      <TableContainer
        component={Paper}
        style={{ maxHeight: "15vh", overflowY: "scroll" }}
      >
        <Table
          className={classes.table}
          size="small"
          aria-label="a dense table"
        >
          <TableHead>
            <TableRow>
              <StyledTableCell>Available Bikes</StyledTableCell>
              <StyledTableCell align="center">Available Stands</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {realInfo.map((info) => {
              return (
                <StyledTableRow key={info.idA + info.idB}>
                  <StyledTableCell align="center">
                    {/* bikesAvailable */}
                    {info.targetB}
                  </StyledTableCell>
                  {/* docksAvailable */}
                  <StyledTableCell align="center">
                    {info.targetA}
                  </StyledTableCell>
                </StyledTableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    );
  } else {
    // tabular information for airports
    return (
      <TableContainer
        component={Paper}
        // style={{ overflowY: "scroll" }}
      >
        <div style={{ paddingBottom: "1vh" }}>
          <Button
            size="small"
            variant="contained"
            disableElevation
            onClick={() => {
              props.setAirportDepartureFlag(true);
              props.setAirportArrivalFlag(false);
            }}
          >
            Departures
          </Button>
          <Button
            size="small"
            variant="contained"
            disableElevation
            onClick={() => {
              props.setAirportDepartureFlag(false);
              props.setAirportArrivalFlag(true);
            }}
          >
            Arrivals
          </Button>
        </div>
        <Table
          className={classes.table}
          size="small"
          aria-label="a dense table"
        >
          <TableHead>
            <TableRow>
              <StyledTableCell>Airline Name</StyledTableCell>
              <StyledTableCell align="center">Flight Code</StyledTableCell>
              <StyledTableCell align="center">Destination</StyledTableCell>
              <StyledTableCell align="center">
                Scheduled Departure/Arrival
              </StyledTableCell>
              <StyledTableCell align="center">Status</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {realInfo.map((info) => {
              return (
                <StyledTableRow key={info.idA + info.idB}>
                  <StyledTableCell align="center">
                    {/* airline_name */}
                    {info.targetB}
                  </StyledTableCell>
                  {/* Flight Code */}
                  <StyledTableCell align="center">{info.idB}</StyledTableCell>
                  <StyledTableCell align="center">
                    {/* Destination */}
                    {info.targetA}
                  </StyledTableCell>
                  {/* Scheduled Departure */}
                  <StyledTableCell align="center">{info.idA}</StyledTableCell>
                  {/* Status */}
                  <StyledTableCell align="center">
                    {info.targetC}
                  </StyledTableCell>
                </StyledTableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
};

export default LocationInformation;

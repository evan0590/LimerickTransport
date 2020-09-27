// Importing outside developed components.
import React from "react";
// Promise based HTTP client - https://github.com/axios/axios.
const axios = require("axios");

// Makes GET request to Django API with user selected stopid as parameter.
// Django makes GET request to the RTPI API, which React returns as a Table.
// Clicking a bus stop's marker will display this Table.
const TestAPI = (props) => {
  // The response from the backend we need to track in state:
  const [data, setData] = React.useState({ apiResponse: "" });

  // The Effect Hook used to perform side effects in this component.
  // https://reactjs.org/docs/hooks-effect.html.
  React.useEffect(
    () => {
      const CancelToken = axios.CancelToken;
      const source = CancelToken.source();
      const loadData = () => {
        try {
          axios.get(`/testAPI`).then((res) => {
            setData({ apiResponse: res.data });
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
    []
  ); // react-hooks/exhaustive-deps

  return (
    <div>
      <p>{data.apiResponse}</p>
    </div>
  );
};

export default TestAPI;

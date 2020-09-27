import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import Avatar from "@material-ui/core/Avatar";
import LocationOnIcon from "@material-ui/icons/LocationOn";
import AddIcon from "@material-ui/icons/Add";
import { blue, green, purple, red, yellow } from "@material-ui/core/colors";

const emails = ["username@gmail.com", "user02@gmail.com"];

const transportModes = [
  "Airport",
  "Railway Station",
  "Bus Stop",
  "Bike Station",
];
const transportIcons = [
  "http://maps.google.com/mapfiles/ms/icons/purple-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
];
const transportColors = [purple[500], red[500], green[500], yellow[500]];
const transportObjects = [
  {
    transportMode: "Airport",
    iconColor: purple[500],
  },
  {
    transportMode: "Railway Station",
    iconColor: red[500],
  },
  {
    transportMode: "Bus Stop",
    iconColor: green[500],
  },
  {
    transportMode: "Bike Station",
    iconColor: yellow[500],
  },
];

const useStyles = makeStyles({
  avatar: {
    backgroundColor: blue[100],
    color: blue[600],
  },
});

export default function CustomDialog(props) {
  const classes = useStyles();
  const handleClose = () => {
    props.setDialogOpen(false);
  };

  const string =
    "This application allows users to view information related to air, " +
    "rail, bus and bike transport services in Limerick and the wider Mid-Western region." +
    " This information is gathered from various APIs and data sources " +
    "and presented in tabular format upon a user clicking on a marker.";

  if (props.dialogFlag === true) {
    return (
      <React.Fragment>
        <Dialog
          maxWidth={"sm"}
          open={props.dialogOpen}
          onClose={handleClose}
          aria-labelledby="max-width-dialog-title"
        >
          <DialogTitle id="max-width-dialog-title">About</DialogTitle>
          <DialogContent>
            <DialogContentText>{string}</DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </React.Fragment>
    );
  } else
    return (
      <React.Fragment>
        <Dialog
          maxWidth={"sm"}
          open={props.dialogOpen}
          onClose={handleClose}
          aria-labelledby="max-width-dialog-title"
        >
          <DialogTitle id="max-width-dialog-title">Key</DialogTitle>
          <List>
            {transportObjects.map((data, idx) => (
              <ListItem key={idx}>
                <ListItemAvatar>
                  <Avatar className={classes.avatar}>
                    <LocationOnIcon style={{ color: data.iconColor }} />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary={data.transportMode} />
              </ListItem>
            ))}
          </List>
        </Dialog>
      </React.Fragment>
    );
}

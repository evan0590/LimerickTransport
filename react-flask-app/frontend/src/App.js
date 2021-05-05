import React, { useState } from "react";
import clsx from "clsx";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import CssBaseline from "@material-ui/core/CssBaseline";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import SubjectIcon from "@material-ui/icons/Subject";
import LocationOnIcon from "@material-ui/icons/LocationOn";

import Weather from "simple-react-weather";

import Map from "./components/Map";
import CustomDialog from "./components/CustomDialog";

import "./App.css";

const drawerWidth = 240;

// Latitude and longitude coordinates are: 52.668018, -8.630498.
const limerickCenter = require("./data/LimerickCenter.json");
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    display: "flex",
  },
  appBar: {
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  hide: {
    display: "none",
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerHeader: {
    display: "flex",
    alignItems: "center",
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
    justifyContent: "flex-end",
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: -drawerWidth,
  },
  contentShift: {
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  },
  title: {
    flexGrow: 1,
  },
}));

export default function App() {
  const classes = useStyles();
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [dialogFlag, setDialogFlag] = React.useState();
  // latitude and longitude variable saved in state.
  const [lat, setLat] = useState(limerickCenter.lat);
  const [lng, setLng] = useState(limerickCenter.lng);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleDialogOpen = () => {
    console.log();
    setDialogOpen(true);
  };

  const handleDialogFlag = (bool) => {
    setDialogFlag(bool);
  };

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        position="fixed"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            className={clsx(classes.menuButton, open && classes.hide)}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            className={classes.title}
            onClick={() => window.location.reload(false)}
            style={{ cursor: "pointer" }}
          >
            Limerick & Mid-West Travel Information
          </Typography>

          <Weather
            // Inbuilt props: https://github.com/lopogo59/simple-react-weather#readme.
            unit="C"
            lat={lat}
            lon={lng}
            appid={process.env.REACT_APP_WEATHER_API}
            style={{
              paddingTop: "1vh",
            }}
          />
        </Toolbar>
      </AppBar>
      <Drawer
        className={classes.drawer}
        variant="persistent"
        anchor="left"
        open={open}
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <div className={classes.drawerHeader}>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "ltr" ? (
              <ChevronLeftIcon />
            ) : (
              <ChevronRightIcon />
            )}
          </IconButton>
        </div>
        <Divider />
        <List>
          <ListItem
            button
            key={"About"}
            onClick={() => {
              handleDialogOpen();
              handleDialogFlag(true);
            }}
          >
            <ListItemIcon>
              <SubjectIcon />
            </ListItemIcon>
            <ListItemText primary={"About"} />
          </ListItem>
          <ListItem
            button
            key={"Key"}
            onClick={() => {
              handleDialogOpen();
              handleDialogFlag(false);
            }}
          >
            <ListItemIcon>
              <LocationOnIcon />
            </ListItemIcon>
            <ListItemText primary={"Key"} />
          </ListItem>
        </List>
        {/* <List>
          {["About", "Legend"].map((text, index) => (
            <ListItem button key={text} onClick={handleDialogOpen}>
              <ListItemIcon>
                {index % 2 === 0 ? <SubjectIcon /> : <LocationOnIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List> */}
        <CustomDialog
          dialogOpen={dialogOpen}
          setDialogOpen={setDialogOpen}
          dialogFlag={dialogFlag}
          setDialogFlag={setDialogFlag}
        ></CustomDialog>
        <Divider />
      </Drawer>
      <main
        className={clsx(classes.content, {
          [classes.contentShift]: open,
        })}
      >
        <div className={classes.drawerHeader} />
        {/* Render the Google Map */}
        <Map setLat={setLat} setLng={setLng}></Map>
      </main>
    </div>
  );
}

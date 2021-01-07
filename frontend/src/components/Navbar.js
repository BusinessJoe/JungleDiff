import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { Link } from "react-router-dom";

  export default function Navbar() {
          return (
                <div>
                    <AppBar position="static">
                        <Grid item xs={12} align = "center" styles={{flexGrow: 1}}>
                            <Typography variant='h2' component={Link} to="/" style ={{textDecoration: 'none', color: 'white'}}>League Api Lads</Typography>
                        </Grid>
                        <Grid item xs={12} align="center">
                            <ButtonGroup variant="contained" size="small" fullWidth="true">
                                <Button variant="contained" style={{ backgroundColor: "#a6d4fa" }}>
                                    <Typography>Something1</Typography>
                                </Button>
                                <Button variant="contained" style={{ backgroundColor: "#a6d4fa" }}>
                                    <Typography>Something2</Typography>
                                </Button>
                                <Button variant="contained" style={{ backgroundColor: "#a6d4fa" }} >
                                    <Typography>Something3</Typography>
                                </Button>
                            </ButtonGroup>
                        </Grid>
                    </AppBar>
                </div>
          )
  }
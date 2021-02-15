import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div>
      <AppBar position="static" style = {{ backgroundColor: "#2066d6" }}>
        <Grid item xs={12} align = "center" styles={{flexGrow: 1}}>
          <Typography
            variant='h2'
            component={Link}
            to="/"
            style={{textDecoration: 'none', color: 'white'}}
          >
            JungleDiff
          </Typography>
        </Grid>
      </AppBar>
    </div>
  )
}

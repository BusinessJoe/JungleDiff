import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import Navbar from './Navbar';
import ChartTest from './ChartTest';
import DragonGoldDiffChart from './Charts.js';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

export default class SummonerPage extends Component {
  constructor(props) {
    super (props);

    this.state = {
      Location:  props.location.state,
      data: {
        datasets: null,
      }
    }
  }

  render() {
    return (
      <Grid container spacing ={0}>
        <Grid item xs = {12}>
          <Navbar />
        </Grid>
        <Grid item xs = {12}>
          <DragonGoldDiffChart Location={this.state.Location}/>
        </Grid>
      </Grid>
    );
  }
}

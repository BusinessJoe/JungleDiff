import { React, Component } from 'react';
import { Grid, Typography, TextField, Paper } from '@material-ui/core';
import Navbar from './Navbar';
import ChartTest from './ChartTest';
import DragonGoldDiffChart from './Charts.js';
import axios from 'axios';
import './SummonerPage.css';

axios.defaults.baseURL = 'http://localhost:8000';

export default class SummonerPage extends Component {
  constructor(props) {
    super (props);

    this.state = {
      ...props.location.state,
      data: {
        datasets: null,
      }
    }
  }

  render() {
    return (
      <div>
        <Navbar />
        <Paper id='contentwrapper'>
          <Grid container>
            <Grid item xs={2}>
              <img
                className='summonericon'
                src='https://cdn3.volusion.com/hckyx.hepad/v/vspfiles/photos/CONC-REDAPPLE-2.jpg?v-cache=1396136943'
              />
            </Grid>
            <Grid item>
              {this.state.summoner_name}
            </Grid>
          </Grid>
          <Grid container>
            <Grid item xs={12} sm={6}>
              <DragonGoldDiffChart Location={this.state.Location}/>
            </Grid>
            <Grid item xs={12} sm={6}>
              Graph explanation
            </Grid>
          </Grid>
        </Paper>
      </div>
    );
  }
}

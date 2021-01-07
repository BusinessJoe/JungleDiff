import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import Navbar from './Navbar';
import ChartTest from './ChartTest';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

export default class SummonerPage extends Component {
  constructor(props) {
    super (props);

    this.state = {
      data: {
        datasets: []
      }
    }
  }

  componentDidMount() {
    axios.get('api/summoner/JJamali/graph/dragon-gold-diff')
    .then(({ data }) => {
      this.setState({
        data: {
          datasets: [data]
        }
      });
    })
    .catch((err) => {});


  }

  render() {
    return (
      <Grid container spacing ={0}>
        <Grid item xs = {12}>
          <Navbar />
        </Grid>
        <Grid item xs = {12}>
          <ChartTest data={this.state.data}/>
        </Grid>
      </Grid>
    );
  }
}

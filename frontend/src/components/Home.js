import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import axios from 'axios';
import './Home.css'

axios.defaults.baseURL = 'http://localhost:8000';

export default class Home extends Component {
  enterPressed(e) {
    var code = e.keyCode || e.which;
    if(code === 13) {
      axios.post("/api/summoner/", {
        summoner_name: e.target.value,
      })
      .then(response => {
        console.log(response);
        this.props.history.push({
          pathname: "/summonerPage/" + e.target.value,
          state: {summoner_data: response.data}
        })
      })
      .catch(error => {
        console.log(error);
      });
    }
  }

  render() {
    return (
      <div className="page-container">
        <div
          style={{
            position: 'absolute', left: '50%', top: '50%',
            transform: 'translate(-50%, -50%)', backgroundColor: 'white',
            padding: '20px',
            borderRadius: '10px',
            opacity: '0.8',
          }}
          className="content"
          >
          <Grid container spacing={3} className="center" direction="row" align="center" justify="center">
            <Grid item xs={12} align="center">
              <Typography variant="h3" compact="h3">
                JungleDiff
              </Typography>
            </Grid>
            <Grid item xs={12} align="center">
              <TextField id="outlined-basic" label="Search Summoner" variant="outlined" fullWidth={true} onKeyPress={this.enterPressed.bind(this)}/>
            </Grid>
          </Grid>
        </div>
        <footer className="footer">
          <div className="footer-content">[JungleDiff] © 2021 [JungleDiff] isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
          </div>
        </footer>
      </div>
    );
  }
}

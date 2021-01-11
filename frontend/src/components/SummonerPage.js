import { React, Component } from 'react';
import { Grid, Typography, TextField, Paper } from '@material-ui/core';
import Navbar from './Navbar';
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

  getSummonerIcon() {
    const iconId = this.state.profile_icon_id;
    return `http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/${iconId}.png`
  }

  render() {
    return (
      <div className='page-container'>
        <Navbar />
        <div className='content'>
          <Paper id='content-paper'>
            <Grid container>
              <Grid item xs={3} md={2} lg={1}>
                <div className='center'>
                    <img
                      className='summoner-icon'
                      src={this.getSummonerIcon()}
                    />
                </div>
              </Grid>
              <Grid item className='v-center'>
                <Typography className='sumName'>{this.state.summoner_name}</Typography>
              </Grid>
            </Grid>
            <Grid container>
              <Grid item xs={12} sm={6}>
                <DragonGoldDiffChart Location={this.state.Location}/>
              </Grid>
              <Grid item xs={12} sm={6} className='text-container'>
                <p className='plaintext'>
                  This graph represents your predicted chances of securing the
                  first dragon based on data from your last 30 ranked games and
                  compares it to the average diamond game.
                </p>
                <p className='plaintext'>
                  For example, the average diamond player has a 50% chance of
                  securing the first dragon if the botlane is perfectly even
                  (0 gold difference). This chance grows to 75% if
                  botlane is 300 gold ahead.
                </p>
              </Grid>
            </Grid>
          </Paper>
        </div>
        <footer className='footer'>
          <div className='footer-content'>
            [JungleDiff] © 2021 [JungleDiff] isn’t endorsed by Riot Games and
            doesn’t reflect the views or opinions of Riot Games or anyone
            officially involved in producing or managing League of Legends.
            League of Legends and Riot Games are trademarks or registered
            trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
          </div>
        </footer>
      </div>
    );
  }
}

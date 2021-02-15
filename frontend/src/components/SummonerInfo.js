import { Component } from 'react';
import { Grid, Typography } from '@material-ui/core';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

export default class SummonerInfo extends Component {
  getSummonerIcon() {
    const iconId = this.props.summoner_data.profile_icon_id;
    return `http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/${iconId}.png`
  }

  render() {
    return (
      <Grid container>
        <Grid item xs={3} md={2} lg={1}>
          <div className='center'>
              <img
                className='summoner-icon'
                src={this.getSummonerIcon()}
                alt='Summoner icon'
              />
          </div>
        </Grid>
        <Grid item className='v-center' xs>
          <Typography className='sumName'>
            {this.props.summoner_data.summoner_name}
          </Typography>
        </Grid>
      </Grid>
    );
  }
}

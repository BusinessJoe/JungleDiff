import { React, Component } from 'react';
import { Grid, Paper } from '@material-ui/core';
import Navbar from './Navbar';
import DragonGoldDiffChart from './Charts.js';
import SummonerInfo from './SummonerInfo.js';
import axios from 'axios';
import './SummonerPage.css';

axios.defaults.baseURL = 'http://localhost:8000';

export default class SummonerPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: {
        datasets: null,
      }
    };
  }

  componentDidMount() {
    if (typeof this.props.location.state !== 'undefined') {
      let summoner_data = this.props.location.state.summoner_data;
      this.setState({summoner_data: summoner_data});
      console.log('not undefined')
      console.log(summoner_data);
      console.log(this.state);
    }
    else {
      let name = this.props.match.params.summonerName;
      axios.get('api/summoner', {params: {summoner_name: name}})
      .then(response => {
        this.setState({summoner_data: response.data});
        console.log('undefined');
        console.log(response.data);
        console.log(this.state);
      });
    }
  }

  render() {
    return (
      <div className='page-container'>
        <Navbar />
        <div className='content'>
          <Paper id='content-paper'>
            {this.state.summoner_data &&
              <SummonerInfo summoner_data={this.state.summoner_data} />
            }
            {this.state.summoner_data &&
              <Grid container>
                <Grid item xs={12} sm={6}>
                  <DragonGoldDiffChart summonerName={this.state.summoner_data.summoner_name}/>
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
            }
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

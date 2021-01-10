import { Component } from 'react';
import { Scatter } from 'react-chartjs-2';
import axios from 'axios';


export default class DragonGoldDiffChart extends Component {
  constructor(props) {
    super(props);

    this.state = {
      summonerData: null,
      comparisonData: null,
    };
  }

  componentDidMount() {
    // get summoner data
    axios.get(`${this.props.Location}graph/dragon-gold-diff`)
    .then(({ data }) => {
      this.setState({
        summonerData : data
      });
    })
    .catch((err) => {console.log(err);});

    // get comparison datasets
    axios.get('/api/comparison/graph/dragon-gold-diff/')
    .then(({ data }) => {
      data.backgroundColor = '#AAAAAA';
      this.setState({
        comparisonData : data
      });
    })
    .catch((err) => {console.log(err);});
  }

  render() {
    var chartData = {};
    if (this.state.summonerData && this.state.comparisonData) {
      chartData = {
        datasets:[this.state.summonerData, this.state.comparisonData]
      }
    }

    const chartOptions = {
      title: {
        display: true,
        text: 'First Dragon Chance vs Botlane Gold Diff @ 10 mins',
      },
      aspectRatio: 1.5,
      scales: {
        xAxes: [{
          ticks: {
            min: -500,
            max: 500,
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 1,
          }
        }]
      }
    }

    // Null width and height are required for aspectRatio to work
    return (
      <Scatter
        data={chartData}
        height={null}
        width={null}
        options={chartOptions}
      />
    )
  }
}

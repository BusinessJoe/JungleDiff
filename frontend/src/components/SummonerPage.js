import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import Navbar from './Navbar';
import ChartTest from './ChartTest';

export default class SummonerPage extends Component {
    constructor(props) {
        super (props);
    }

    render() {
        return (
            <Grid container spacing ={0}>
               <Grid item xs = {12}>
                    <Navbar />
                </Grid>
                <Grid item xs = {12}>
                    <ChartTest />
                </Grid>
            </Grid>
        );
    }
}
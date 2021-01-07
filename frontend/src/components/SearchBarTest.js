import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import Navbar from './Navbar';

export default class SearchTest extends Component {
    constructor(props) {
        super (props);
    }

    render() {
        return (
            <div
            style={{
                position: 'absolute', left: '50%', top: '50%',
                transform: 'translate(-50%, -50%)'
            }}
            >
                <Navbar />
                <Grid container spacing={3} className="center">
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" compact="h3">
                            SearchBar Pog
                        </Typography>
                    </Grid>
                </Grid>
            </div>
        );
    }
}
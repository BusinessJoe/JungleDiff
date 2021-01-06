import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';

export default class Home extends Component {
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
                <Grid container spacing={3} className="center">
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" compact="h3">
                            League API Lads
                        </Typography>
                    </Grid>
                    <Grid item xs={12} direction="row" align="center" justify="center">
                        <TextField id="outlined-basic" label="Search Summoner" variant="outlined" fullWidth="true" onKeyPress={this.enterPressed.bind(this)}/>   
                    </Grid>
                </Grid>
            </div>
        );
    }
}
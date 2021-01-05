import { React, Component } from 'react';
import { Grid, Typography, TextField } from '@material-ui/core';
import axios from 'axios';

export default class Home extends Component {
    constructor(props) {
        super (props);
    }

    enterPressed(e) {
        var code = e.keyCode || e.which;
        if(code === 13) {
            axios.post("/api/summoner/", {
                    summoner_name: e.target.value,    
                })
            .then((response) => {
                if (response.ok) {
                    this.props.history.push("/test/" + e.target.value);
                }
                else {
                    console.log(response);
                    //throw new Error();
                }
            });
        }
    }

    render() {
        return (
            <div
            style={{
                position: 'absolute', left: '50%', top: '50%',
                transform: 'translate(-50%, -50%)',
            }}
            >
                <Grid container spacing={3} className="center" direction="row" align="center" justify="center">
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" compact="h3">
                            League API Lads
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <TextField id="outlined-basic" label="Search Summoner" variant="outlined" fullWidth={true} onKeyPress={this.enterPressed.bind(this)}/>   
                    </Grid>
                </Grid>
            </div>
        );
    }
}
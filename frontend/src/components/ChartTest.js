import React from 'react';
import { Scatter } from 'react-chartjs-2';


export default function ChartTest(props) {
    return (
        <Scatter data={props.data} options={
            {
              title: {
                display: true,
                text: 'Scatter',
              },
              legend: {
                display: false,
              },
            }}/>
    );
}

import React from 'react';
import { Line } from 'react-chartjs-2';


export default function ChartTest() {
    const data = {
        labels: ['100g', '200g', '300g', '400g', '500g'],
        datasets: [
            {
                label: 'Bot gold vs Dragon Secure',
                data: [1, 2, 2, 3 ,5],
            },
            {
                label: 'Blah blah balh',
                data: [2,4,5,1,1],
            }
        ]
    }
    return (
        <Line data={data} />
    );
}
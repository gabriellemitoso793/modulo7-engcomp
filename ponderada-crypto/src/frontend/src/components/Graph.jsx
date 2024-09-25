import React from 'react';
import { Line } from 'react-chartjs-2';

const Graph = ({ data }) => {
    const chartData = {
        labels: data.holt_winters_forecast.map((_, index) => `Dia ${index + 1}`),
        datasets: [
            {
                label: 'Previsão de Preço',
                data: data.holt_winters_forecast,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            },
        ],
    };

    return (
        <div className="card mt-4">
            <div className="card-body">
                <h5 className="card-title">Gráfico de Previsão</h5>
                <Line data={chartData} />
            </div>
        </div>
    );
};

export default Graph;

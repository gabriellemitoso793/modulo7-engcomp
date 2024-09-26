import React from 'react';
import { Line } from 'react-chartjs-2';

const Graph = ({ data }) => {
    if (!data || !data.holt_winters_forecast) {
        return <div>No data available</div>;
    }

    const chartData = {
        labels: data.holt_winters_forecast.map((_, index) => `Dia ${index + 1}`),
        datasets: [
            {
                label: 'Previsão de Preço',
                data: data.holt_winters_forecast,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.4,  // Curva mais suave
            },
        ],
    };

    const options = {
        scales: {
            y: {
                beginAtZero: false,
                ticks: {
                    callback: function(value) {
                        return `$${value}`;
                    }
                }
            }
        }
    };

    return (
        <div className="card mt-4">
            <div className="card-body">
                <h5 className="card-title">Gráfico de Previsão de Preço</h5>
                <Line data={chartData} options={options} />
            </div>
        </div>
    );
};

export default Graph;

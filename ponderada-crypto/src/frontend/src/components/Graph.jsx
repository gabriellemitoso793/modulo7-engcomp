import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    Filler,
    CategoryScale
} from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, Title, Tooltip, Legend, Filler, CategoryScale);

const Graph = ({ forecast }) => {
    if (!forecast || !forecast.previsao_dias || forecast.previsao_dias.length === 0) {
        return <div>No data available</div>;
    }

    const chartData = {
        labels: forecast.previsao_dias.map((_, index) => `Dia ${index + 1}`),
        datasets: [
            {
                label: 'Previsão de Preço',
                data: forecast.previsao_dias.map(dia => dia.forecast_price),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const options = {
        scales: {
            x: { 
                type: 'category',
                title: {
                    display: true,
                    text: 'Dias',
                },
            },
            y: {
                beginAtZero: false,
                ticks: {
                    callback: function(value) {
                        return `$${value}`;
                    }
                },
                title: {
                    display: true,
                    text: 'Preço',
                },
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

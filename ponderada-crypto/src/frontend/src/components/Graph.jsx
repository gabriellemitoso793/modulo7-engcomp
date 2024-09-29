import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const Graph = ({ holt_winters_forecast = [] }) => {
    const hasData = holt_winters_forecast.length > 0;

    if (!hasData) {
        return <div className="alert alert-warning" role="alert">Carregando gráfico...</div>;
    }

    const data = {
        labels: Array.from({ length: holt_winters_forecast.length }, (_, i) => `Dia ${i + 1}`),
        datasets: [
            {
                label: 'Previsão Holt-Winters',
                data: holt_winters_forecast,
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                tension: 0.4,
                pointBackgroundColor: 'rgba(153, 102, 255, 1)',
                pointBorderColor: '#fff',
                pointHoverRadius: 7,
                fill: true,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    color: '#333',
                    font: {
                        size: 14,
                    },
                },
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += parseFloat(context.raw).toFixed(4);
                        return label;
                    },
                },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: '#333',
                },
                grid: {
                    display: false,
                },
            },
            y: {
                ticks: {
                    color: '#333',
                },
                grid: {
                    color: 'rgba(200, 200, 200, 0.2)',
                },
            },
        },
    };

    return (
        <div style={{ height: '400px' }}>
            <h3>Gráfico de Previsão</h3>
            <Line data={data} options={options} />
        </div>
    );
};

export default Graph;
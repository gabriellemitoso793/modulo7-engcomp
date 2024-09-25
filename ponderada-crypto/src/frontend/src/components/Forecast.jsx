import React from 'react';

const Forecast = ({ forecast }) => {
    return (
        <div className="card mt-4">
            <div className="card-body">
                <h5 className="card-title">Previsão dos Próximos 5 Dias</h5>
                <ul className="list-group list-group-flush">
                    {forecast.map((day, index) => (
                        <li className="list-group-item" key={index}>
                            <strong>Dia:</strong> {day.date} <br />
                            <strong>Preço Previsto:</strong> {day.forecast_price.toFixed(2)} <br />
                            <strong>Sinal de Compra:</strong> {day.buy_signal ? 'Sim' : 'Não'}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Forecast;

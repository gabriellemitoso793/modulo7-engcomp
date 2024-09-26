import React from 'react';

const Forecast = ({ forecast }) => {
    if (!forecast || !forecast.melhores_dias || !forecast.previsao_dias) {
        return <div>No data available</div>;
    }

    return (
        <div className="card mt-4">
            <div className="card-body">
                <h5 className="card-title">Previsões de Preço e Volatilidade</h5>

                <h6 className="mt-4">Melhores Dias</h6>
                {forecast.melhores_dias.map((dia, index) => (
                    <div key={index} className="mb-3">
                        <strong>Preço Previsto:</strong> ${dia.forecast_price.toFixed(2)} <br/>
                        <strong>Volatilidade Prevista:</strong> {dia.forecast_volatility.toFixed(6)} <br/>
                        <strong>Sinal de Compra:</strong> {dia.buy_signal ? 'Sim' : 'Não'}
                    </div>
                ))}

                <h6 className="mt-4">Previsão para os Próximos Dias</h6>
                {forecast.previsao_dias.map((dia, index) => (
                    <div key={index} className="mb-3">
                        <strong>Preço Previsto:</strong> ${dia.forecast_price.toFixed(2)} <br/>
                        <strong>Volatilidade Prevista:</strong> {dia.forecast_volatility.toFixed(6)}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Forecast;


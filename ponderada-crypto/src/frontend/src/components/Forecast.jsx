import React from 'react';

const Forecast = ({ forecast }) => {
    if (!forecast || !forecast.melhores_dias || !forecast.previsao_dias) {
        return <div className="alert alert-warning" role="alert">No data available</div>;
    }

    return (
        <div className="card mt-4">
            <div className="card-body">
                <h5 className="card-title">Previsões de Preço e Volatilidade</h5>

                {/* Melhor Dia */}
                <h6 className="mt-4">Melhor Dia</h6>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Preço Previsto</th>
                            <th>Volatilidade Prevista</th>
                            <th>Vale a pena comprar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {forecast.melhores_dias.map((dia, index) => (
                            <tr key={index}>
                                <td>${dia.forecast_price.toFixed(2)}</td>
                                <td>{dia.forecast_volatility.toFixed(6)}</td>
                                <td>{dia.buy_signal ? 'Sim' : 'Não'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Previsão para os Próximos Dias */}
                <h6 className="mt-4">Previsão para os Próximos Dias</h6>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Dia</th>
                            <th>Preço Previsto</th>
                            <th>Volatilidade Prevista</th>
                        </tr>
                    </thead>
                    <tbody>
                        {forecast.previsao_dias.map((dia, index) => (
                            <tr key={index}>
                                <td>{`Dia ${index + 1}`}</td>
                                <td>${dia.forecast_price.toFixed(2)}</td>
                                <td>{dia.forecast_volatility.toFixed(6)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Forecast;

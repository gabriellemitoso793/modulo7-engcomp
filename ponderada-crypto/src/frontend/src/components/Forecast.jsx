const Forecast = ({ cryptoData }) => {
    if (!cryptoData) {
        return <div className="alert alert-warning" role="alert">Carregando dados...</div>;
    }

    const { melhores_dias, holt_winters_forecast } = cryptoData;

    if (!melhores_dias || !holt_winters_forecast) {
        return <div className="alert alert-danger" role="alert">Dados não encontrados.</div>;
    }

    const convertTimestampToDate = (timestamp) => {
        return new Date(timestamp).toLocaleDateString('pt-BR');
    };

    return (
        <div className="forecast-container">
            <h3 className="forecast-title">Previsão de Preços e Melhores Dias</h3>

            {melhores_dias.length > 0 ? (
                <div className="section">
                    <h4 className="section-title">Melhores Dias para Comprar</h4>
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            {melhores_dias.map((dia, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{convertTimestampToDate(dia)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="alert alert-info" role="alert">Nenhum dia ideal encontrado.</div>
            )}

            <div className="section">
                <h4 className="section-title">Valores Previstos para os Próximos Dias (Holt-Winters)</h4>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Data</th>
                            <th>Valor Previsto</th>
                        </tr>
                    </thead>
                    <tbody>
                        {holt_winters_forecast.map((valorPrevisto, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td>{new Date(Date.now() + index * 24 * 60 * 60 * 1000).toLocaleDateString('pt-BR')}</td>
                                <td>{valorPrevisto.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Forecast;

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ForecastComponent = () => {
    const [forecastData, setForecastData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/executarmodelo');
                setForecastData(response.data.dates);
            } catch (error) {
                console.error("Erro ao buscar os dados: ", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!forecastData) {
        return <div>No data available</div>;
    }

    return (
        <div>
            <h2>Previsões de Bitcoin</h2>
            <h3>Melhores Dias</h3>
            {forecastData.bitcoin.melhores_dias.map((dia, index) => (
                <div key={index}>
                    <p>Preço Previsto: {dia.forecast_price}</p>
                    <p>Volatilidade Prevista: {dia.forecast_volatility}</p>
                    <p>Sinal de Compra: {dia.buy_signal ? 'Sim' : 'Não'}</p>
                </div>
            ))}

            <h3>Previsão Próximos Dias</h3>
            {forecastData.bitcoin.previsao_dias.map((dia, index) => (
                <div key={index}>
                    <p>Preço Previsto: {dia.forecast_price}</p>
                    <p>Volatilidade Prevista: {dia.forecast_volatility}</p>
                </div>
            ))}

            <h2>Previsões de Ethereum</h2>
            <h3>Melhores Dias</h3>
            {forecastData.ethereum.melhores_dias.map((dia, index) => (
                <div key={index}>
                    <p>Preço Previsto: {dia.forecast_price}</p>
                    <p>Volatilidade Prevista: {dia.forecast_volatility}</p>
                    <p>Sinal de Compra: {dia.buy_signal ? 'Sim' : 'Não'}</p>
                </div>
            ))}

            <h3>Previsão Próximos Dias</h3>
            {forecastData.ethereum.previsao_dias.map((dia, index) => (
                <div key={index}>
                    <p>Preço Previsto: {dia.forecast_price}</p>
                    <p>Volatilidade Prevista: {dia.forecast_volatility}</p>
                </div>
            ))}
        </div>
    );
};

export default ForecastComponent;

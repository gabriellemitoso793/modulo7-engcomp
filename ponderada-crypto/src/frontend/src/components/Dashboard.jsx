import React, { useEffect, useState } from 'react';
import { fetchCryptoData } from '../api';
import Forecast from './Forecast';
import Graph from './Graph';
import CryptoSelector from './CryptoSelector';
import './Dashboard.css';

const Dashboard = () => {
    const [selectedCrypto, setSelectedCrypto] = useState('bitcoin');
    const [cryptoData, setCryptoData] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            const data = await fetchCryptoData();
            setCryptoData(data.resultado[selectedCrypto.charAt(0).toUpperCase() + selectedCrypto.slice(1)]);
        };

        loadData();
    }, [selectedCrypto]);

    return (
        <div className="dashboard-container">
            <h2 className="dashboard-title"></h2>
            <CryptoSelector selectedCrypto={selectedCrypto} setSelectedCrypto={setSelectedCrypto} />
            {cryptoData ? (
                <div className="dashboard-content">
                    <Forecast cryptoData={cryptoData} />
                    <Graph 
                        holt_winters_forecast={cryptoData.holt_winters_forecast}
                    />
                </div>
            ) : (
                <div className="loading-alert alert alert-warning" role="alert">
                    Carregando dados...
                </div>
            )}
        </div>
    );
};

export default Dashboard;

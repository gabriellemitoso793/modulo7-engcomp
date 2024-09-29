import React, { useEffect, useState } from 'react';
import { fetchCryptoData } from '../api';
import Forecast from './Forecast';
import Graph from './Graph';
import CryptoSelector from './CryptoSelector';

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
        <div>
            <h2>Dashboard</h2>
            <CryptoSelector selectedCrypto={selectedCrypto} setSelectedCrypto={setSelectedCrypto} />
            {cryptoData ? (
                <>
                    <Forecast cryptoData={cryptoData} />
                    <Graph 
                        holt_winters_forecast={cryptoData.holt_winters_forecast}
                    />
                </>
            ) : (
                <div className="alert alert-warning" role="alert">Carregando dados...</div>
            )}
        </div>
    );
};

export default Dashboard;
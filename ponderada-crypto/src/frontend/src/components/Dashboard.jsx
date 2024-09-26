import React, { useState, useEffect } from 'react';
import CryptoSelector from './CryptoSelector';
import Graph from './Graph';
import Forecast from './Forecast';
import Loading from './Loading';
import { fetchCryptoData } from '../api';

const Dashboard = () => {
    const [selectedCrypto, setSelectedCrypto] = useState('bitcoin');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getData = async () => {
            setLoading(true);
            try {
                const result = await fetchCryptoData(selectedCrypto);
                setData(result);
            } catch (error) {
                console.error("Erro ao buscar dados da API", error);
            } finally {
                setLoading(false);
            }
        };

        getData();
    }, [selectedCrypto]);

    if (loading) return <Loading />;

    if (!data || !data.dates || !data.dates[selectedCrypto]) {
        return <div>No data available</div>;
    }

    return (
        <div className="container">
            <CryptoSelector selectedCrypto={selectedCrypto} setSelectedCrypto={setSelectedCrypto} />
            <div className="row">
                <div className="col-lg-6">
                    <Graph data={data.dates[selectedCrypto]} />
                </div>
                <div className="col-lg-6">
                    <Forecast forecast={data.dates[selectedCrypto]} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;

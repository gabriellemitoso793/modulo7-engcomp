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
            const result = await fetchCryptoData(selectedCrypto);
            setData(result);
            setLoading(false);
        };

        getData();
    }, [selectedCrypto]);

    if (loading) return <Loading />;

    return (
        <div className="container">
            <CryptoSelector selectedCrypto={selectedCrypto} setSelectedCrypto={setSelectedCrypto} />
            <div className="row">
                <div className="col-lg-6">
                    <Graph data={data} />
                </div>
                <div className="col-lg-6">
                    <Forecast forecast={data.dates[selectedCrypto]} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;

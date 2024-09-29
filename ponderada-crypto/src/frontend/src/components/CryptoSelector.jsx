import React from 'react';

const CryptoSelector = ({ selectedCrypto, setSelectedCrypto }) => {
  return (
    <div className="text-center my-4">
      <h2 className="mb-4">Selecione a Criptomoeda</h2>
      <div>
        <button
          className={`btn btn-outline-primary mx-2 ${selectedCrypto === 'bitcoin' ? 'active' : ''}`}
          onClick={() => setSelectedCrypto('bitcoin')}
        >
          <i className="fab fa-bitcoin"></i> Bitcoin
        </button>
        <button
          className={`btn btn-outline-success mx-2 ${selectedCrypto === 'ethereum' ? 'active' : ''}`}
          onClick={() => setSelectedCrypto('ethereum')}
        >
          <i className="fab fa-ethereum"></i> Ethereum
        </button>
      </div>
    </div>
  );
};

export default CryptoSelector;
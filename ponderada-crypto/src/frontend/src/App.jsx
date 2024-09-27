import React from 'react';
import Dashboard from './components/Dashboard';

const App = () => {
    return (
        <>
            <header className="text-center my-4">
                <h1>Previsão de Criptomoedas</h1>
            </header>
            <main className="container">
                <Dashboard />
            </main>
        </>
    );
};

export default App;

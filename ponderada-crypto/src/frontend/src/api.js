const API_URL = 'http://localhost:8000';

export const fetchCryptoData = async () => {
    console.log("Fetching data for Bitcoin and Ethereum");
    const response = await fetch(`${API_URL}/executarmodelo`);
    if (!response.ok) {
        console.error('Erro ao buscar dados da API');
        throw new Error('Erro ao buscar dados da API');
    }
    const data = await response.json();
    console.log('Data fetched successfully:', data);
    return data;
};

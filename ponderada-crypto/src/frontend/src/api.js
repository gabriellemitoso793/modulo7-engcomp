const API_URL = 'http://localhost:8000';

export const fetchCryptoData = async (crypto) => {
    console.log(`Fetching data for: ${crypto}`);
    const response = await fetch(`${API_URL}/executarmodelo?crypto=${crypto}`);
    if (!response.ok) {
        console.error('Erro ao buscar dados da API');
        throw new Error('Erro ao buscar dados da API');
    }
    const data = await response.json();
    console.log('Data fetched successfully:', data);
    return data; 
};

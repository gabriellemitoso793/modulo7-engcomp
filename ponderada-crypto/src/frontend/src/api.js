const API_URL = 'http://localhost:8000';

export const fetchCryptoData = async (crypto) => {
    const response = await fetch(`${API_URL}/executarmodelo?crypto=${crypto}`);
    if (!response.ok) {
        throw new Error('Erro ao buscar dados da API');
    }
    const data = await response.json();
    return data; 
};

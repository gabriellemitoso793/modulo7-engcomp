const API_URL = 'http://backend:8000'; // Mude localhost para backend

export const fetchCryptoData = async (crypto) => {
    const response = await fetch(`${API_URL}/executarmodelo`);
    if (!response.ok) {
        throw new Error('Erro ao buscar dados da API');
    }
    const data = await response.json();
    return data; // Ajuste conforme necessário
};

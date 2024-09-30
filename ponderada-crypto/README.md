# Ponderada-Crypto

O projeto **Ponderada-Crypto** é uma aplicação web full-stack que permite prever o melhor dia para comprar criptomoedas (Bitcoin e Ethereum) com base na volatilidade e no preço previsto, utilizando modelos estatísticos e de machine learning, como GARCH, ARIMA e Holt-Winters.

## Índice
- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Dependências](#dependências)
- [Modelos Utilizados](#modelos-utilizados)
- [Arquitetura de Microserviços](#arquitetura-de-microserviços)

## Visão Geral

O sistema coleta dados da API da Coingecko das criptomoedas e os processa para gerar previsões de preço e volatilidade, além de sugerir os melhores dias para compra. A aplicação conta com um frontend em React para exibir as previsões e um backend desenvolvido em FastAPI que executa os modelos e processa os dados.

## Estrutura do Projeto

```bash
ponderada-crypto/
│
├── backend/
│   ├── main.py                # Código principal
│   ├── modelo.py              # Código com os modelos GARCH, ARIMA, Holt-Winters
│   ├── Dockerfile             # Arquivo Dockerfile do backend
│   ├── requirements.txt       # Dependências do backend 
│   ├── config.py              # Configurações do caminho de arquivos e outras
│   ├── retreinarmodelo.py      # Script para retreinar os modelos
│   ├── database/
│   │   └── dados-puros/
│   │       ├── crypto_data.db  # Banco de dados com os dados de criptomoedas
│   │       └── collect_data.py # Script para coletar dados de criptomoedas
    │   └── dados-processados/
│   │       ├── analise-exploratoria-btc.ipynb  # Análise exploratória de Bitcoin
│   │       └── analise-exploratoria-eth.ipynb  # Análise exploratória de Ethereum
│   ├── utils/
│   │   ├── file_handler.py     # Funções auxiliares para manipulação de arquivos (upload, etc.)
│   │   └── processar.py        # Funções auxiliares para processar resultados dos modelos
│   └── logs/                  # Logs para monitoramento do sistema
│       └── app.log            # Arquivo de log do sistema
│ 
├── frontend/
│   ├── public/                # Diretório público para assets estáticos
│   │   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx   # Componente do Dashboard
│   │   │   ├── CryptoSelector.jsx # Componente para selecionar Bitcoin/Ethereum
│   │   │   ├── Graph.jsx       # Componente para gráficos
│   │   │   ├── Forecast.jsx    # Componente para previsões
│   │   │   └── Loading.jsx     # Componente de loading
│   │   │   └── Dashboard.css   # Estilos para o Dashboard
│   │   │   └── Forecast.css    # Estilos para o Forecast
│   │   ├── App.jsx            # Componente principal do React
│   │   ├── index.js           # Ponto de entrada do React
│   │   └── api.js             # Funções para chamadas à API do backend
│   ├── package.json           # Dependências do frontend 
│   ├── Dockerfile             # Arquivo Dockerfile do frontend
│   └── node_modules/          # Módulos instalados do Node.js
│
├── docker-compose.yml          # Arquivo Docker Compose para orquestrar frontend e backend
├── package.json                # Dependências do projeto
├── crypto_data.db              # Banco de dados de criptomoedas
├── package-lock.json           # Controle de versões das dependências Node.js 
└── README.md                   # Documentação do projeto
```

## Instalação

### Requisitos

- Docker e Docker Compose instalados na máquina
- Python 3.10+
- Node.js 18+

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/gabriellemitoso793/modulo7-engcomp.git
cd ponderada-crypto
```

2. Inicialize o backend e o frontend com Docker Compose:

```bash
docker-compose up --build
```

3. O frontend estará disponível em http://localhost:3000 e o backend em http://localhost:8000.

## Uso Interface Web
A interface web permite que você selecione uma criptomoeda (Bitcoin ou Ethereum) e visualize as previsões de volatilidade e preço, além dos melhores dias para comprar com base nas previsões geradas pelos modelos.

## Modelos
O modelo padrão mostrado na interface puxa os dados de um banco de dados já feito, entretanto, você pode retreinar os modelos manualmente executando o script:

```bash
python backend/retreinarmodelo.py
```

## Dependências

### Backend (backend/requirements.txt):
    - fastapi: Framework web para construir o backend.
    - arch: Implementação do modelo GARCH.
    - statsmodels: Utilizado para os modelos ARIMA e Holt-Winters.
    - pandas, numpy, scikit-learn: Manipulação de dados e pré-processamento.
    - matplotlib, seaborn: Visualização de dados para análise.
    
### Frontend (frontend/package.json):
    - React: Biblioteca para construir a interface de usuário.
    - Axios: Utilizado para chamadas à API.
    - Bootstrap: Estilos e layout responsivo.

## Modelos Utilizados

- GARCH (Generalized Autoregressive Conditional Heteroskedasticity):
Utilizado para prever a volatilidade dos preços de criptomoedas.

- ARIMA (Autoregressive Integrated Moving Average):
Modelo de série temporal utilizado para prever os preços futuros com base nos dados históricos.

- Holt-Winters (Exponential Smoothing):
Modelo para previsão sazonal, usado para complementar as previsões de preços.

## Arquitetura de Microserviços

O Ponderada-Crypto adota uma arquitetura baseada em microserviços para garantir modularidade e facilidade de manutenção. A aplicação é dividida em dois serviços principais, cada um executando uma parte específica da lógica do sistema:

Neste projeto, dois microserviços principais foram configurados:

### Backend

- Desenvolvido em FastAPI, este serviço processa os dados de preço e volatilidade de criptomoedas (Bitcoin e Ethereum) e os expõe via uma API REST.
- Ele se comunica diretamente com o banco de dados e utiliza modelos preditivos (GARCH, ARIMA, Holt-Winters) para gerar as previsões de preço e volatilidade.
- Porta de acesso: 8000.

### Frontend:

- Desenvolvido em React, o frontend é responsável por exibir as informações para o usuário final, como gráficos de preços e recomendações de compra.
- Ele consome as APIs fornecidas pelo backend para obter as previsões e visualizá-las de forma interativa.
- Porta de acesso: 3000.

Ambos os serviços estão conectados pela rede Docker chamada crypto_network, o que permite a comunicação eficiente entre eles.
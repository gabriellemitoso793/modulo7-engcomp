ponderada-crypto/
│
├── backend/
│   ├── main.py                # Código principal do FastAPI
│   ├── modelo.py              # Código com os modelos GARCH, ARIMA, Holt-Winters
│   ├── Dockerfile             # Arquivo Dockerfile do backend
│   ├── requirements.txt       # Dependências do backend (FastAPI, pandas, etc.)
│   ├── config.py              # Configurações do caminho de arquivos e outras
│   ├── database/
│   │   └── dados-puros/
│   │       ├── bitcoin_daily_data.csv
│   │       └── ethereum_daily_data.csv
│   │       └── collect_data.py
    │   └── dados-processados/
│   │       ├── analise-exploratoria-btc.ipynb
│   │       └── analise-exploratoria-eth.ipynb
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
│   │   ├── App.jsx            # Componente principal do React
│   │   ├── index.js           # Ponto de entrada do React
│   │   └── api.js             # Funções para chamadas à API do backend
│   ├── package.json           # Dependências do frontend (React, Bootstrap, etc.)
│   ├── Dockerfile             # Arquivo Dockerfile do frontend
│   └── node_modules/          # Módulos instalados do Node.js
│
├── docker-compose.yml          # Arquivo Docker Compose para orquestrar frontend e backend
├── package.json
├── crypto_data.db           
├── package-lock.json           # Arquivo Docker Compose para orquestrar frontend e backend 
└── README.md                   # Documentação do projeto

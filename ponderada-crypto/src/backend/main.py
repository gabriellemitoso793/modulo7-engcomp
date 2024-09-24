from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from modelo import executar_modelo
from utils.file_handler import save_file
from config import DATA_DIR
from utils.processar import processar_resultado

# Configuração do logging
logging.basicConfig(
    filename="/home/gabriellemitoso/modulo7-engcomp/ponderada-crypto/src/backend/logs/app.log",  # Caminho do arquivo de log
    level=logging.INFO,        # Nível de logging
    format="%(asctime)s %(levelname)s: %(message)s",  # Formato da mensagem
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data
)

app = FastAPI()

# Configura o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["http://localhost:8000"]
)

# Rota simples de teste
@app.get("/hello")
def principal():
    logging.info("Rota '/hello' acessada.")
    return {"message": "Hello, World!"}

# Rota para upload de arquivo
@app.post("/inserirbase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = save_file(file, DATA_DIR)
        logging.info(f"Arquivo '{file.filename}' salvo com sucesso em {file_location}.")
        return {"info": f"Arquivo '{file.filename}' salvo com sucesso em {file_location}"}
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

# Rota para execução do modelo
@app.get("/executarmodelo")
def modelo():
    try:
        resultado = executar_modelo()
        if not resultado or len(resultado) < 2:
            raise ValueError("O resultado do modelo está vazio ou inválido.")
        
        message, dates = processar_resultado(resultado)
        logging.info("Modelo executado com sucesso.")
        return {"message": message, "dates": dates}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo: {str(e)}")

# Início do servidor
if __name__ == "__main__":
    logging.info("Iniciando o servidor...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

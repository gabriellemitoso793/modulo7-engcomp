import uvicorn
import logging
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from modelo import executar_modelo
from utils.file_handler import save_file
from config import DATA_DIR
from utils.processar import processar_resultado

# Configuração do diretório de logs
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração do logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["*"]
)

@app.get("/hello")
def principal():
    logging.info("Rota '/hello' acessada.")
    return {"message": "Hello, World!"}

@app.post("/inserirbase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = save_file(file, DATA_DIR)
        logging.info(f"Arquivo '{file.filename}' salvo com sucesso em {file_location}.")
        return {"info": f"Arquivo '{file.filename}' salvo com sucesso em {file_location}"}
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

@app.get("/executarmodelo")
def modelo():
    try:
        logging.info("Iniciando a execução do modelo.")
        resultado = executar_modelo()

        # Log do resultado
        logging.info(f"Resultado do modelo: {resultado}")
        
        if not resultado or len(resultado) < 2:
            raise ValueError("O resultado do modelo está vazio ou inválido.")

        message, dates = processar_resultado(resultado)

        # Log dos dados processados
        logging.info(f"Dados processados: {dates}")

        logging.info("Modelo executado com sucesso.")
        return {"message": message, "dates": dates}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

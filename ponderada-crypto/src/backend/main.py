from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from modelo import executar_modelo
import re
import uvicorn

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIRECTORY = BASE_DIR / "database"
UPLOAD_DIRECTORY.mkdir(exist_ok=True) 

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
    return {"message": "Hello, World!"}

# Rota para upload de arquivo
@app.post("/inserirbase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIRECTORY / file.filename
        
        # Abre o arquivo e grava no diretório
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"info": f"Arquivo '{file.filename}' salvo com sucesso em {file_location}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

# Função auxiliar para processar o resultado do modelo
def processar_resultado(resultado):
    # Inicializa variáveis
    message = ""
    dias_certos = []
    erros = 0

    # Divide o resultado e verifica as condições
    for item in resultado[1].split():
        if 'False' in item:
            erros += 1
        elif 'True' in item:
            dias_certos.append(item)

    # Define a mensagem com base nos erros
    if erros > 3:
        message = "Essa semana não é recomendada para comprar Bitcoin."
    else:
        message = f"Semana recomendada para comprar Bitcoin nos dias: {' '.join(dias_certos)}"
    
    # Busca e retorna as datas do resultado
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, resultado[0])

    return message, dates

# Rota para execução do modelo
@app.get("/executarmodelo")
def modelo():
    try:
        resultado = executar_modelo()
        if not resultado or len(resultado) < 2:
            raise ValueError("O resultado do modelo está vazio ou inválido.")
        
        message, dates = processar_resultado(resultado)
        return {"message": message, "dates": dates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo: {str(e)}")

# Início do servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

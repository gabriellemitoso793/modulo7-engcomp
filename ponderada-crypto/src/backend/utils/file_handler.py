import os
from fastapi import UploadFile
from config import DATA_DIR
from pathlib import Path

# Função para salvar o arquivo enviado no diretório
def save_file(file: UploadFile, data_dir: Path = DATA_DIR) -> str:

    #Cria o diretório se ele não existir
    os.makedirs(data_dir, exist_ok=True)

    #Define o caminho onde o arquivo será salvo
    file_location = data_dir / file.filename

    #Salva o arquivo
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_location)  #Retorna o caminho

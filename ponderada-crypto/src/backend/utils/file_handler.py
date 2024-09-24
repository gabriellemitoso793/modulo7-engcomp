from pathlib import Path
import shutil
from fastapi import UploadFile

def save_file(file: UploadFile, upload_dir: Path):
    file_location = upload_dir / file.filename
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    except Exception as e:
        raise Exception(f"Erro ao salvar o arquivo: {str(e)}")

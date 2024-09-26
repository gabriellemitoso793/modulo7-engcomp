import os
from fastapi import UploadFile
from config import DATA_DIR

def save_file(file: UploadFile, data_dir: str) -> str:

    # Create the directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    # Define the path where the file will be saved
    file_location = os.path.join(data_dir, file.filename)

    # Save the file
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    return file_location

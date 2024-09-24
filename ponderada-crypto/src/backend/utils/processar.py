# utils/processar.py

def processar_resultado(resultado) -> tuple[str, list]:
    # Exemplo de processamento do resultado
    message = "Processamento realizado com sucesso."
    dates = [str(data) for data in resultado]  # Exemplo de transformação
    return message, dates

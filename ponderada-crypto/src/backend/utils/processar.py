import logging

def processar_resultado(resultados: dict) -> tuple:
    """
    Processa os resultados do modelo e prepara os dados para retorno.
    """
    logging.info(f"Resultados recebidos para processamento: {resultados}")

    try:
        melhores_dias_btc = resultados['bitcoin']['melhores_dias']
        previsao_dias_btc = resultados['bitcoin']['previsao_proximos_dias']
        holt_winters_forecast_btc = resultados['bitcoin']['holt_winters_forecast']

        melhores_dias_eth = resultados['ethereum']['melhores_dias']
        previsao_dias_eth = resultados['ethereum']['previsao_proximos_dias']
        holt_winters_forecast_eth = resultados['ethereum']['holt_winters_forecast']

        message = "Processamento realizado com sucesso!"
        
        dates = {
            "bitcoin": {
                "melhores_dias": melhores_dias_btc.to_dict(orient='records'),  
                "previsao_dias": previsao_dias_btc.to_dict(orient='records'),  
                "holt_winters_forecast": holt_winters_forecast_btc
            },
            "ethereum": {
                "melhores_dias": melhores_dias_eth.to_dict(orient='records'),  
                "previsao_dias": previsao_dias_eth.to_dict(orient='records'),  
                "holt_winters_forecast": holt_winters_forecast_eth
            }
        }

        return message, dates
    except Exception as e:
        logging.error(f"Erro ao processar os resultados: {e}")
        raise ValueError(f"Erro ao processar os resultados: {str(e)}")

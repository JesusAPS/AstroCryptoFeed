import os
import requests
from utils.logger import setup_logger

logger = setup_logger()

# Endpoint Oficial de Binance Square (OpenAPI)
BASE_URL = 'https://www.binance.com'
ENDPOINT = '/bapi/composite/v1/public/pgc/openApi/content/add'

def publish_to_binance_square(content):
    """
    Publica contenido en Binance Square usando la OpenAPI oficial de Square.
    Requiere una API Key generada específicamente para Binance Square.
    """
    # Leer la API Key en tiempo de ejecución (no al importar) para robustez
    api_key = os.getenv('BINANCE_SQUARE_API_KEY') or os.getenv('BINANCE_API_KEY')

    if not api_key:
        logger.error("Falta la BINANCE_SQUARE_API_KEY en las variables de entorno")
        return False, "Falta API Key"

    # Log de diagnóstico (solo longitud para seguridad)
    logger.info(f"Diagnóstico: API Key de Square cargada (Longitud: {len(api_key)})")

    url = BASE_URL + ENDPOINT

    # Encabezado correcto confirmado: X-Square-OpenAPI-Key
    headers = {
        'X-Square-OpenAPI-Key': api_key,
        'clienttype': 'binanceSkill',
        'Content-Type': 'application/json'
    }

    # El cuerpo de la petición (JSON)
    payload = {
        'bodyTextOnly': content
    }

    try:
        logger.info("Enviando publicación a la API Oficial de Binance Square...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ Publicación exitosa en Binance Square.")
                return True, data
            else:
                logger.error(f"❌ Error de negocio de Binance: {data}")
                return False, str(data)
        else:
            logger.error(f"❌ Error HTTP ({response.status_code}): {response.text}")
            return False, response.text

    except Exception as e:
        logger.error(f"Excepción al publicar en Binance Square: {e}")
        return False, str(e)


import os
import requests
from utils.logger import setup_logger

logger = setup_logger()

# Configuración API Binance Square
BINANCE_SQUARE_API_KEY = os.getenv('BINANCE_SQUARE_API_KEY')

# Endpoint Oficial de Binance Square (OpenAPI)
BASE_URL = 'https://www.binance.com'
ENDPOINT = '/bapi/composite/v1/public/pgc/openApi/content/add'

def publish_to_binance_square(content):
    """
    Publica contenido en Binance Square usando la OpenAPI oficial de Square.
    Requiere una API Key generada específicamente para Binance Square.
    """
    if not BINANCE_SQUARE_API_KEY:
        logger.error("Falta la BINANCE_SQUARE_API_KEY en el .env")
        return False, "Falta API Key"

    # Log de diagnóstico (solo longitud para seguridad)
    logger.info(f"Diagnóstico: BINANCE_SQUARE_API_KEY cargada (Longitud: {len(BINANCE_SQUARE_API_KEY)})")

    url = BASE_URL + ENDPOINT

    # Encabezados requeridos para Binance Square OpenAPI
    headers = {
        'X-Square-Api-Key': BINANCE_SQUARE_API_KEY,
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


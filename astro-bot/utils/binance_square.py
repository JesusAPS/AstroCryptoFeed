import os
import time
import requests
import hashlib
import hmac
from urllib.parse import urlencode
from utils.logger import setup_logger

logger = setup_logger()

# Configuración API Binance
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Endpoint Base para Creadores/Square (Dependiendo del acceso, este puede variar)
# Según la doc general de Binance para APIs firmadas, empieza con api.binance.com
BASE_URL = 'https://api.binance.com' 

def generate_signature(query_string, secret):
    """Genera la firma HMAC-SHA256 requerida por Binance."""
    return hmac.new(
        secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def publish_to_binance_square(content):
    """
    Intenta publicar contenido en Binance Square usando la API oficial firmada.
    Requiere que la API Key tenga permisos de 'Binance Feed/Square Creator'.
    """
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        logger.error("Faltan las credenciales API de Binance en el .env")
        return False, "Faltan credenciales API"

    # NOTA IMPORTANTE: El endpoint exacto para "Crear Post" en Square 
    # a través de la API pública suele estar restringido a Partners.
    # Usaremos el endpoint estándar documentado para contenido estructurado.
    endpoint = '/sapi/v1/bpay/content/create' # <-- Este endpoint es un placeholder común,
                                              # se debe ajustar al endpoint exacto otorgado por Binance
    url = BASE_URL + endpoint

    timestamp = int(time.time() * 1000)
    
    # Parámetros obligatorios (ajustar según la doc oficial otorgada al usuario)
    params = {
        'content': content,
        'timestamp': timestamp
    }
    
    query_string = urlencode(params)
    signature = generate_signature(query_string, BINANCE_API_SECRET)
    
    # Añadir firma al final
    params['signature'] = signature

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        logger.info("Intentando publicar en Binance Square vía API...")
        # Nota: Usamos requests.post, algunos endpoints requieren requests.get con params
        response = requests.post(url, headers=headers, params=params)
        
        if response.status_code == 200:
            logger.info("Publicación exitosa en Binance Square.")
            return True, response.json()
        else:
            logger.error(f"Error Binance API ({response.status_code}): {response.text}")
            return False, response.text

    except Exception as e:
        logger.error(f"Excepción al publicar en Binance Square: {e}")
        return False, str(e)

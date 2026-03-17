import requests
from utils.format import log_event

def get_fear_and_greed():
    """Obtiene el índice de Miedo y Codicia de Alternative.me"""
    url = "https://api.alternative.me/fng/"
    try:
        response = requests.get(url)
        data = response.json()
        val = data['data'][0]
        return {
            'value': int(val['value']),
            'sentiment': val['value_classification']
        }
    except Exception as e:
        log_event(f"Error Fear & Greed: {e}", "error")
        return None

def get_binance_long_short_ratio(symbol='BTCUSDT', period='1h'):
    """Obtiene el ratio Long/Short de cuentas de Binance (Sentimiento de Whale/Top Traders)"""
    # Nota: Esta es una URL de la API de Binance Futures para datos de sentimiento
    url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}&period={period}&limit=1"
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return {
                'symbol': symbol,
                'long_short_ratio': float(data[0]['longShortRatio']),
                'long_account': float(data[0]['longAccount']),
                'short_account': float(data[0]['shortAccount'])
            }
        return None
    except Exception as e:
        log_event(f"Error Long/Short Ratio: {e}", "error")
        return None

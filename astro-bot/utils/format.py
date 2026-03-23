from datetime import datetime

def log_event(message, status="info"):
    emoji = {"info": "🛰️", "success": "✅", "error": "❌"}.get(status, "🔧")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {emoji} {message}")

def get_crypto_tags(asset_name):
    """
    Genera hashtags y cashtags para un activo cripto.
    Ejemplo: 'BTCUSDT' -> '$BTC', '#BTC #Crypto #Binance'
    """
    # Limpiar el nombre (quitar USDT si es de Binance)
    clean_name = asset_name.replace('USDT', '').upper()
    
    cashtag = f"${clean_name}"
    hashtags = f"#{clean_name} #Crypto #Blockchain #AstroBot"
    
    return cashtag, hashtags

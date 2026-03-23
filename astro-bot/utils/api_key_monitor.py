import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def check_api_key_expiry():
    """Verifica si la API Key de Binance Square está próxima a expirar y alerta."""
    created_date_str = os.getenv('BINANCE_SQUARE_KEY_CREATED', '')
    
    if not created_date_str:
        logger.info("ℹ️ BINANCE_SQUARE_KEY_CREATED no configurada. No se verificará expiración.")
        return
    
    try:
        created_date = datetime.strptime(created_date_str, '%Y-%m-%d')
        expiry_date = created_date + timedelta(days=30)
        days_left = (expiry_date - datetime.now()).days
        
        if days_left <= 5:
            from utils.notify import send_telegram_alert
            if days_left <= 0:
                send_telegram_alert(
                    f"🔑 *API Key de Binance Square EXPIRADA*\n"
                    f"Creada: `{created_date_str}`\n"
                    f"Genera una nueva en Binance → Square → OpenAPI Settings"
                )
            else:
                send_telegram_alert(
                    f"⚠️ *API Key de Binance Square expira en {days_left} días*\n"
                    f"Creada: `{created_date_str}`\n"
                    f"Renuévala pronto en Binance → Square → OpenAPI Settings"
                )
            logger.warning(f"⚠️ API Key de Square: {days_left} días para expirar")
        else:
            logger.info(f"🔑 API Key de Square válida ({days_left} días restantes)")
    except ValueError:
        logger.error(f"Formato inválido para BINANCE_SQUARE_KEY_CREATED: {created_date_str}. Usa YYYY-MM-DD")

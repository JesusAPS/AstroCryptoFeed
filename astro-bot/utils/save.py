import pandas as pd
from datetime import datetime
from utils.format import log_event
from utils.database import get_engine, CryptoPrice
from sqlalchemy.orm import sessionmaker

def save_data(data, filename=None): # filename se mantiene por compatibilidad pero se ignora
    if data:
        try:
            engine = get_engine()
            Session = sessionmaker(bind=engine)
            session = Session()

            # Preparar objeto
            new_price = CryptoPrice(
                symbol=data.get('symbol') or data.get('token'),
                price=data['price'],
                change_24h=data['change'],
                volume=data.get('volume'),
                rsi=data.get('rsi'),
                fear_greed=data.get('fear_greed'),
                long_short_ratio=data.get('long_short_ratio'),
                source="Binance" if 'symbol' in data else "CoinGecko"
            )

            session.add(new_price)
            session.commit()
            session.close()
            
            # log_event(f"Datos guardados en DB para {new_price.symbol}", "success")
        except Exception as e:
            log_event(f"Error guardando en DB: {e}", "error")

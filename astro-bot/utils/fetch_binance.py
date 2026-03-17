import pandas as pd
from binance.client import Client
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET
from utils.format import log_event

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_binance_data(symbol='BTCUSDT'):
    try:
        ticker = client.get_ticker(symbol=symbol)
        return {
            'symbol': symbol,
            'price': float(ticker['lastPrice']),
            'change': float(ticker['priceChangePercent']),
            'volume': float(ticker['volume'])
        }
    except Exception as e:
        log_event(f"Error Binance Ticker: {e}", "error")
        return None

def get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=100):
    """
    Obtiene velas históricas para análisis técnico.
    Devuelve DataFrame con columnas: timestamp, open, high, low, close, volume
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        data = []
        for k in klines:
            data.append({
                'timestamp': k[0],
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            })
        return pd.DataFrame(data)
    except Exception as e:
        log_event(f"Error Binance Klines: {e}", "error")
        return pd.DataFrame()

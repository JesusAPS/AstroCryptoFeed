import pandas as pd
from sqlalchemy import create_engine

# Ruta compartida
DB_PATH = 'sqlite:////app/shared/data/crypto_data.db'

def get_engine():
    return create_engine(DB_PATH)

def load_data_from_db(source, symbol=None, limit=100):
    try:
        engine = get_engine()
        if symbol:
            query = f"SELECT * FROM prices WHERE source='{source}' AND symbol='{symbol}' ORDER BY timestamp DESC LIMIT {limit}"
        else:
            query = f"SELECT * FROM prices WHERE source='{source}' ORDER BY timestamp DESC LIMIT {limit}"
            
        df = pd.read_sql(query, engine)
        return df.sort_values(by='timestamp')
    except Exception as e:
        return pd.DataFrame()

def get_available_symbols(source):
    try:
        engine = get_engine()
        query = f"SELECT DISTINCT symbol FROM prices WHERE source='{source}' ORDER BY symbol"
        df = pd.read_sql(query, engine)
        return df['symbol'].tolist()
    except:
        return []

def load_binance_data(symbol=None, limit=100):
    return load_data_from_db("Binance", symbol, limit)

def load_coingecko_data(symbol=None, limit=100):
    return load_data_from_db("CoinGecko", symbol, limit)

def get_aligned_prices(source="Binance", limit=500):
    """
    Obtiene los precios de todos los símbolos, los alinea por timestamp
    (resampleando por horas) para calcular correlaciones.
    """
    symbols = get_available_symbols(source)
    prices_dict = {}
    for sym in symbols:
        df = load_data_from_db(source, sym, limit)
        if not df.empty:
            # Resample de la serie temporal por horas para alinear datos
            # Técnicas de Pandas vitales para el Data Analysis
            df_sym = df.set_index('timestamp').resample('1h')['price'].last()
            prices_dict[sym] = df_sym
            
    if prices_dict:
        return pd.DataFrame(prices_dict).dropna()
    return pd.DataFrame()

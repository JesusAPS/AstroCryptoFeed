import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands

def calculate_technical_indicators(df):
    """
    Calcula indicadores técnicos sobre un DataFrame de velas (Klines).
    Se usa para evaluar la tendencia y volatilidad de un activo, ideal para Data Analysis EDA.
    Se espera que el DataFrame tenga una columna 'close'.
    """
    if df.empty:
        return None

    # RSI (Relative Strength Index) - 14 periodos para medir momentum
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()
    
    # SMA (Media Móvil Simple) - 20 periodos para tendencia suavizada
    sma_indicator = SMAIndicator(close=df['close'], window=20)
    df['sma_20'] = sma_indicator.sma_indicator()
    
    # EMA (Media Móvil Exponencial) - 20 periodos dando peso a precios recientes
    ema_indicator = EMAIndicator(close=df['close'], window=20)
    df['ema_20'] = ema_indicator.ema_indicator()
    
    # Bollinger Bands - 20 periodos, 2 desviaciones estándar para medir volatilidad
    bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_high'] = bb_indicator.bollinger_hband()
    df['bb_low'] = bb_indicator.bollinger_lband()
    df['bb_mid'] = bb_indicator.bollinger_mavg()
    
    return df

def get_signal(rsi_value):
    """
    Devuelve una señal basada en el valor del RSI.
    """
    if rsi_value is None:
        return "NEUTRAL", "⚪"
        
    if rsi_value < 30:
        return "SOBREVENTA (Compra)", "🟢"
    elif rsi_value > 70:
        return "SOBRECOMPRA (Venta)", "🔴"
    else:
        return "NEUTRAL", "⚪"

import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands

def calculate_technical_indicators(df):
    """
    Aquí es donde aplico la ciencia financiera para sacar el RSI, SMA y demás inventos.
    Necesito que el DataFrame tenga una columna 'close' para poder trabajar.
    """
    if df.empty:
        return None

    # El RSI (Fuerza) - Uso 14 periodos para ver si el mercado está eufórico o deprimido
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()
    
    # Media Móvil Simple (SMA) - 20 periodos para ver la tendencia sin tanto ruido
    sma_indicator = SMAIndicator(close=df['close'], window=20)
    df['sma_20'] = sma_indicator.sma_indicator()
    
    # Media Móvil Exponencial (EMA) - Le da más importancia a lo que pasó hace un ratito
    ema_indicator = EMAIndicator(close=df['close'], window=20)
    df['ema_20'] = ema_indicator.ema_indicator()
    
    # Bandas de Bollinger - Mi radar de volatilidad para ver hasta dónde puede llegar el precio
    bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_high'] = bb_indicator.bollinger_hband()
    df['bb_low'] = bb_indicator.bollinger_lband()
    df['bb_mid'] = bb_indicator.bollinger_mavg()
    
    return df

def get_signal(rsi_value):
    """
    Una función rápida para que el bot me diga qué hacer dependiendo del RSI.
    """
    if rsi_value is None:
        return "NEUTRAL", "⚪"
        
    if rsi_value < 30:
        return "SOBREVENTA (Compra)", "🟢"
    elif rsi_value > 70:
        return "SOBRECOMPRA (Venta)", "🔴"
    else:
        return "NEUTRAL", "⚪"

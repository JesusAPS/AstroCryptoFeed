from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Ruta de la base de datos (relativa al directorio actual, compatible con nube local)
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared', 'data')
DB_PATH = f'sqlite:///{os.path.join(DB_DIR, "crypto_data.db")}'

Base = declarative_base()

class CryptoPrice(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    symbol = Column(String)       # Ej: BTCUSDT, ethereum
    price = Column(Float)
    change_24h = Column(Float)
    volume = Column(Float, nullable=True)
    rsi = Column(Float, nullable=True)
    fear_greed = Column(Integer, nullable=True)
    long_short_ratio = Column(Float, nullable=True)
    source = Column(String)       # Ej: Binance, CoinGecko

def get_engine():
    return create_engine(DB_PATH)

def init_db():
    """Crea las tablas si no existen."""
    os.makedirs(DB_DIR, exist_ok=True)
    engine = get_engine()
    Base.metadata.create_all(engine)

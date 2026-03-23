from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

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

def _migrate_db(engine):
    """Agrega columnas faltantes a tablas existentes (migración automática)."""
    migrations = [
        ("prices", "fear_greed", "INTEGER"),
        ("prices", "long_short_ratio", "REAL"),
    ]
    with engine.connect() as conn:
        for table, column, col_type in migrations:
            try:
                conn.execute(text(f"SELECT {column} FROM {table} LIMIT 1"))
            except Exception:
                logger.info(f"📦 Migrando DB: agregando columna '{column}' a tabla '{table}'")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
                conn.commit()

def init_db():
    """Crea las tablas si no existen y migra columnas faltantes."""
    os.makedirs(DB_DIR, exist_ok=True)
    engine = get_engine()
    Base.metadata.create_all(engine)
    _migrate_db(engine)


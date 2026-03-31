import pandas as pd
from sqlalchemy import create_engine
import os
import sys

# Ajustar el path para poder importar módulos desde la carpeta astro-bot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'astro-bot')))

try:
    from utils.analysis import calculate_technical_indicators
except ImportError:
    print("Asegúrate de ejecutar este script desde la raíz del proyecto o instala los requisitos.")
    sys.exit(1)

# Buscando dónde está la base de datos (Docker o local)
db_relative = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data', 'crypto_data.db')
DB_PATH = f'sqlite:///{os.path.abspath(db_relative)}'

export_relative = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data', 'powerbi_dataset.csv')
EXPORT_PATH = os.path.abspath(export_relative)

def export_data_for_powerbi():
    """
    Extrae datos de SQLite y calcula los indicadores técnicos en lote para Power BI.
    """
    print("🚀 Iniciando exportación y transformación de datos para Power BI...")
    
    engine = create_engine(DB_PATH)
    
    try:
        # 1. Sacando la data de la base de datos (Extract)
        query = "SELECT * FROM prices ORDER BY timestamp ASC"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ No hay datos en la base de datos para exportar.")
            return

        print(f"✅ {len(df)} registros extraídos. Ejecutando el Feature Engineering...")
        
        # 2. Aplicando mi ciencia a los datos (Transform)
        df_processed = pd.DataFrame()
        
        # Separando cada cripto para no mezclar peras con manzanas (BTC vs ETH)
        for symbol in df['symbol'].unique():
            df_sym = df[df['symbol'] == symbol].copy()
            
            # Necesito que la columna se llame 'close' para que la lógica de analysis.py funcione
            df_sym['close'] = df_sym['price']
            
            # Calculando los indicadores financieros (RSI, Medias, etc.)
            df_sym = calculate_technical_indicators(df_sym)
            
            # Borrando las columnas temporales para que el archivo sea ligero
            df_sym = df_sym.drop(columns=['close'])
            
            df_processed = pd.concat([df_processed, df_sym])
            
        # Rellenando los valores nulos (NaN) con Backward Fill
        # para que Power BI no tenga problemas con filas vacías
        df_processed = df_processed.bfill()
        
        # 3. Carga final: Guardar el archivo listo para usar (Load)
        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
        df_processed.to_csv(EXPORT_PATH, index=False)
        
        print(f"🎉 ¡Exportación ETL exitosa! Archivo listo en:\n{EXPORT_PATH}")
        print("💡 Instrucciones para Power BI:")
        print("   1. Abre Power BI Desktop")
        print("   2. Selecciona 'Obtener Datos' -> 'Texto/CSV'")
        print("   3. Selecciona el archivo 'powerbi_dataset.csv'")
        print("   4. ¡Crea tus dashboards gerenciales interactivos!")

    except Exception as e:
        print(f"❌ Error durante el proceso ETL: {e}")

if __name__ == "__main__":
    export_data_for_powerbi()

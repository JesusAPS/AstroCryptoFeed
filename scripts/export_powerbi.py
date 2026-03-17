import pandas as pd
from sqlalchemy import create_engine
import os
import sys

# Ajustar path para importar módulos desde astro-bot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'astro-bot')))

try:
    from utils.analysis import calculate_technical_indicators
except ImportError:
    print("Asegúrate de ejecutar este script desde la raíz del proyecto o instala los requisitos.")
    sys.exit(1)

# Determinar ruta de la BD dependiendo de si estamos en Docker o local
db_relative = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data', 'crypto_data.db')
DB_PATH = f'sqlite:///{os.path.abspath(db_relative)}'

export_relative = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data', 'powerbi_dataset.csv')
EXPORT_PATH = os.path.abspath(export_relative)

def export_data_for_powerbi():
    """
    Extrae datos de SQLite, procesa y calcula indicadores técnicos en batch, y 
    exporta a un CSV limpio ideal para ingestar en Power BI.
    """
    print("🚀 Iniciando exportación y transformación de datos para Power BI...")
    
    engine = create_engine(DB_PATH)
    
    try:
        # 1. Extracción (Extract)
        query = "SELECT * FROM prices ORDER BY timestamp ASC"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ No hay datos en la base de datos para exportar.")
            return

        print(f"✅ {len(df)} registros extraídos. Calculando características (Feature Engineering)...")
        
        # 2. Transformación (Transform)
        df_processed = pd.DataFrame()
        
        # Agrupamos por activo para no mezclar las medias móviles de BTC con ETH
        for symbol in df['symbol'].unique():
            df_sym = df[df['symbol'] == symbol].copy()
            
            # Crear columna 'close' temporalmente para reutilizar la lógica de analysis.py
            df_sym['close'] = df_sym['price']
            
            # Calcular indicadores técnicos
            df_sym = calculate_technical_indicators(df_sym)
            
            # Limpiar columnas innecesarias
            df_sym = df_sym.drop(columns=['close'])
            
            df_processed = pd.concat([df_processed, df_sym])
            
        # Rellenar valores nulos (NaN) generados por los periodos de las medias móviles
        # Usamos backfill para garantizar que Power BI no tenga problemas con filas vacías
        df_processed = df_processed.bfill()
        
        # 3. Carga (Load)
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

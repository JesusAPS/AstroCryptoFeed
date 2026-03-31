import streamlit as st
import pandas as pd
import utils.load_data as load_data
from utils.load_data import load_binance_data, load_coingecko_data, get_aligned_prices
from utils.plot import plot_price_line, plot_candlestick, plot_returns_histogram, plot_correlation_matrix
from utils.format import format_change

import os

st.set_page_config(page_title="AstroCryptoFeed Dashboard", layout="wide")

logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=100)
st.title("🪐 AstroCryptoFeed Dashboard")

st.markdown("_Visualización de datos espaciales y análisis técnico_")

# Dividiendo el dashboard en secciones para organizar mejor la info
tab_monitor, tab_eda = st.tabs(["🔴 Monitor en Vivo", "📊 Análisis Exploratorio (EDA)"])

with tab_monitor:
    st.header("Monitor en Tiempo Real")
    
    # --- SECCIÓN DE BINANCE ---
    st.subheader("🚀 Binance")
    binance_symbols = load_data.get_available_symbols("Binance")
    if binance_symbols:
        selected_binance = st.selectbox("Selecciona Par (Binance)", binance_symbols, index=0)
        binance_df = load_binance_data(selected_binance)
        
        if not binance_df.empty:
            col1, col2, col3 = st.columns(3)
            last_price = binance_df.iloc[-1]['price']
            last_change = binance_df.iloc[-1]['change_24h']
            col1.metric("Precio", f"${last_price}", f"{last_change}%")
            
            st.dataframe(binance_df.tail(5))
            plot_price_line(binance_df, f"{selected_binance} - Precio")

            if 'rsi' in binance_df.columns and pd.notna(binance_df.iloc[-1]['rsi']):
                st.subheader("📊 RSI")
                st.line_chart(binance_df.set_index('timestamp')['rsi'])
                st.metric("RSI Actual", f"{binance_df.iloc[-1]['rsi']:.2f}")
    else:
        st.info("Esperando datos de Binance...")

    # --- SECCIÓN DE COINGECKO ---
    st.subheader("🛰️ CoinGecko")
    cg_symbols = load_data.get_available_symbols("CoinGecko")
    if cg_symbols:
        selected_cg = st.selectbox("Selecciona Token (CoinGecko)", cg_symbols, index=0)
        coingecko_df = load_coingecko_data(selected_cg)
        
        if not coingecko_df.empty:
            col1, col2 = st.columns(2)
            last_price = coingecko_df.iloc[-1]['price']
            last_change = coingecko_df.iloc[-1]['change_24h']
            col1.metric("Precio", f"${last_price}", f"{last_change}%")
            
            st.dataframe(coingecko_df.tail(5))
    else:
        st.info("Esperando datos de CoinGecko...")

with tab_eda:
    st.header("Análisis Exploratorio de Datos (EDA)")
    st.markdown("Esta sección demuestra habilidades de limpieza, transformación y análisis de datos en la serie temporal extraída.")
    
    if binance_symbols:
        eda_symbol = st.selectbox("Activo a Analizar", binance_symbols, index=0, key='eda_sym')
        df_eda = load_binance_data(eda_symbol, limit=2000)
        
        if not df_eda.empty:
            # 1. Transformando los datos de Pandas: Resampling a Velas Japonesas (OHLC)
            st.subheader("1. Transformación OHLC (Velas Japonesas)")
            st.markdown("Agrupando data cruda (ticks) en intervalos de tiempo para visualizar volatilidad mediante Pandas `resample`.")
            # El índice tiene que ser de tiempo para poder graficar
            df_time = df_eda.set_index('timestamp')
            # Agrupando por horas para ver el Open, High, Low y Close
            ohlc_dict = {'price': ['first', 'max', 'min', 'last']}
            df_ohlc = df_time.resample('1h').agg(ohlc_dict)
            df_ohlc.columns = ['open', 'high', 'low', 'close']
            df_ohlc.dropna(inplace=True)
            plot_candlestick(df_ohlc, f"Velas Japonesas (1H) - {eda_symbol}")
            
            # 2. Análisis de Retornos y Volatilidad (Midiendo el riesgo)
            st.subheader("2. Distribución de Retornos y Volatilidad")
            st.markdown("Cálculo del cambio porcentual serie a serie para encontrar distorsiones en el precio (Riesgo).")
            # Calculando el cambio porcentual con Pandas
            df_time['returns'] = df_time['price'].pct_change() * 100
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            volatilidad = df_time['returns'].std()
            media_retorno = df_time['returns'].mean()
            col_stat1.metric("Volatilidad (Desv. Estándar)", f"{volatilidad:.2f}%")
            col_stat2.metric("Retorno Medio", f"{media_retorno:.3f}%")
            col_stat3.metric("Datos Analizados", len(df_time))
            
            plot_returns_histogram(df_time.dropna(subset=['returns']), "Histograma de Retornos (%)")

            # 3. Correlación entre Activos (Viendo si se mueven igual)
            st.subheader("3. Matriz de Correlación entre Activos")
            st.markdown("Análisis matricial para encontrar dependencias lineales entre distintos activos.")
            df_aligned = get_aligned_prices("Binance")
            if not df_aligned.empty and len(df_aligned.columns) > 1:
                col_mat = df_aligned.corr()
                plot_correlation_matrix(col_mat)
            else:
                st.info("No hay suficientes activos con datos solapados para generar correlación.")

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_price_line(df, title="Evolución de Precio"):
    """Dibuja un gráfico de línea interactivo del precio usando Plotly."""
    fig = px.line(df, x='timestamp', y='price', title=title, 
                  labels={'timestamp': 'Fecha', 'price': 'Precio (USD)'})
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

def plot_candlestick(ohlc_df, title="Velas Japonesas"):
    """Dibuja un gráfico de velas japonesas interactivo a partir de un DataFrame OHLC."""
    fig = go.Figure(data=[go.Candlestick(
        x=ohlc_df.index,
        open=ohlc_df['open'],
        high=ohlc_df['high'],
        low=ohlc_df['low'],
        close=ohlc_df['close']
    )])
    fig.update_layout(
        title=title,
        yaxis_title="Precio (USD)",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    # Ocultar rangeselector para que sea más limpio
    fig.update_xaxes(rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_returns_histogram(df, title="Distribución de Retornos"):
    """Dibuja un histograma de los retornos (cambios porcentuales)."""
    fig = px.histogram(df, x='returns', nbins=50, title=title,
                       labels={'returns': 'Retorno Diario (%)'})
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_matrix(corr_df, title="Matriz de Correlación"):
    """Dibuja un Heatmap interactivo de la matriz de correlación."""
    fig = px.imshow(corr_df, text_auto=True, title=title, 
                    color_continuous_scale='RdBu_r', aspect="auto")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

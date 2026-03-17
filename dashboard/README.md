# 📊 Dashboard Web - Análisis Exploratorio de Datos (EDA)

¡Hola desde el Frontend de datos! Esta carpeta contiene la interfaz visual del proyecto **AstroCryptoFeed**. Utilizando **Streamlit**, convertí scripts crudos de Python en un Dashboard Analítico y un Monitor de Trading en vivo de primera calidad. 

## 🧩 ¿Qué encontrarás aquí?

- `dashboard.py` - El script principal. Cuando corres `streamlit run dashboard.py`, este archivo construye todo el sitio web: los conectores, los "estilos" (Tabs, Subheaders, Layout de Metricas) y la interactividad.
- `utils/load_data.py` - El puente entre SQLite y Streamlit, utilizando extensivamente **Pandas** para extraer (`pd.read_sql`) y transformar.
- `utils/plot.py` - El corazón de las visualizaciones interactivas. Todo usando **Plotly**.

---

## 🏗️ Los Problemas que Enfrenté y Cómo los Resolví

### Problema 1: "Una interfaz demasiado saturada"
Al tener datos en vivo y a la vez querer hacer análisis complejos (Análisis Exploratorio), **el problema** inicial fue que la pantalla principal era un caos. Había tantos gráficos que no sabías qué mirar. 
✅ **Mi solución:** Implementé un diseño de pestañas lógicas (Streamlit `Tabs`). Separé magistralmente todo en "Monitor en Vivo" (para que la mirada vaya directa al precio y la acción) y "Análisis Exploratorio (EDA)" (para sentarse a revisar historiales financieros).

### Problema 2: "Los gráficos estáticos se quedan cortos en Finanzas"
Utilicé Matplotlib inicialmente para graficar los datos. **El problema:** No puedes hacer zoom, no puedes ver detalles exactos pasando el ratón, y la verdad es que una gráfica simple en 2D arruinaba por completo la experiencia de uso cuando quieres analizar fluctuaciones pequeñas.
✅ **Mi solución:** Reescribí todo mi módulo `plot.py` e implementé **Plotly**. Pasé de una línea naranja aburrida a elementos interactivos:
1. Gráficos interactivos de Velas Japonesas (Métricas de Apertura/Cierre y Máximos/Mínimos).
2. Histogramas elegantes oscuros para visualizar la distribución del riesgo (Retornos).

### Problema 3: "Combinando Peras con Manzanas en la Matriz de Correlación"
Quería mostrar una **Matriz de Correlación** (un *Heatmap*) entre todas las criptomonedas (Ej: Cuánto se parece el movimiento de BTC al de ETH). **El problema:** Las criptos tienen diferentes horarios exactos de llegada desde la base de datos (desfases de segundos/minutos). Si intentaba cruzar las series temporales con Pandas y no coincidían exactamente, todo daba un error de "Tamaños no alineados", o arrojaba puro `NaN`.
✅ **Mi solución:** Usando un conocimiento profundo de Pandas, utilicé la función de remuestreo de tiempo (`resample('1h')`) acoplada a `.last()`. Esto obligó a que todos los registros de los activos se alinearan limpiamente por hora exacta. Así obtuve un DataFrame cuadrado perfecto, permitiéndome imprimir correlaciones financieras altamente precisas en el mapa de calor de Plotly.

---
*⚠️ **Aviso:** Los gráficos interactivos mostrados en este dashboard son para propósitos de visualización e investigación de datos. **No son recomendaciones de inversión**. El mercado financiero es riesgo 100%.*

# 📊 Dashboard Web - Análisis de Datos con Interfaz

¡Hola desde la parte visual de mi sistema! Esta carpeta tiene la interfaz de **AstroCryptoFeed**. Usé **Streamlit** para pasar de simples scripts analíticos a una web de monitoreo de primera calidad. 📺🛰️

---

## 🧩 ¿Qué hay en esta sección?

- `dashboard.py`: Es el script que arma todo el sitio web. Le da el estilo con pestañas, métricas y los gráficos.
- `utils/load_data.py`: Es como el puente que une SQLite con Streamlit, usando **Pandas** (`pd.read_sql`) de buena forma.
- `utils/plot.py`: Donde nacen los gráficos interactivos usando **Plotly**. ¡Es el corazón visual! ✨📉

---

## 🏗️ Retos Técnicos y Cómo los Solucioné

### 1. Una pantalla muy cargada 😵‍💫
Al principio, los datos en vivo y el historial estaban todos en un solo lugar y no se entendía nada. ¡Un desorden total!
*   **Mi solución:** Usé `Tabs` (pestañas) de Streamlit. Separé todo en "Monitor en Vivo" para ver el precio al momento, y "Análisis Exploratorio (EDA)" para sentarme a ver el pasado con calma. ¡Mucho más ordenado! 🎯

### 2. Los gráficos básicos se quedaban cortos 📉
Empecé usando Matplotlib, pero era muy estático. No podía ver detalles, ni hacer zoom y no se veía tan pro.
*   **Mi solución:** Reescribí todo con **Plotly**. Ahora tengo velas japonesas y gráficos interactivos que se ven fenomenales. ¡Parece un sistema de monitoreo profesional! 😎✨

### 3. ¡Los datos no encajaban en el tiempo! 🧩
Quería hacer una **Matriz de Correlación** (para ver si Bitcoin y Ethereum se mueven igual), pero las fechas no coincidían por segundos y todo daba error.
*   **Mi solución:** Usé mi "magia" con Pandas y el comando `resample('1h')`. Forcé a que todos los datos se alineen perfectamente por hora para que las series temporales cuadraran. ¡Ahora tengo datos limpios y precisos para comparar! 

---
*Nota: Los gráficos son curiosidad científica y para aprender de datos. El mercado real es rudo.* 👨‍💻🛰️

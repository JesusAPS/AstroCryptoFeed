# 📊 Dashboard Web - Análisis de Datos con Onda

¡Hola desde la parte visual de mi laboratorio! Esta carpeta tiene la interfaz de **AstroCryptoFeed**. Usé **Streamlit** para pasar de simples scripts a una web analítica de calidad para ver todo en vivo. 📺🧪

---

## 🧩 ¿Qué inventos hay aquí adentro?

- `dashboard.py`: Es el script que arma todo el sitio web. Le da el estilo con pestañas, métricas y los gráficos.
- `utils/load_data.py`: Es como el puente que une SQLite con Streamlit, usando **Pandas** (`pd.read_sql`) de buena forma.
- `utils/plot.py`: Donde nacen los gráficos interactivos usando **Plotly**. ¡Es el corazón visual!

---

## 🏗️ Retos que me hicieron pensar como un mini científico loco 🧠

### 1. Una pantalla muy cargada 😵‍💫
Al principio, los datos en vivo y el historial estaban todos en un solo lugar y no se entendía nada. ¡Un desorden total!
*   **Mi solución:** Usé `Tabs` (pestañas) de Streamlit. Separé todo en "Monitor en Vivo" para ver el precio al momento, y "Análisis Exploratorio (EDA)" para sentarme a ver el pasado con calma. ¡Mucho más ordenado!

### 2. Los gráficos "aburridos" en 2D 📉
Empecé usando Matplotlib, pero era muy estático. No podía ver detalles, ni hacer zoom, y me sentía en el siglo pasado.
*   **Mi solución:** Reescribí todo con **Plotly**. Ahora tengo velas japonesas y gráficos interactivos que se ven fenomenales. ¡Parece un sistema de trading profesional! 😎

### 3. ¡Los datos no encajan! 🧩
Quería hacer una **Matriz de Correlación** (para ver si Bitcoin y Ethereum se mueven igual), pero las fechas no coincidían por segundos y todo daba error.
*   **Mi solución:** Usé mi "magia" con Pandas y el comando `resample('1h')`. Forcé a que todos los datos se alineen perfectamente por hora. ¡Ahora tengo datos limpios y precisos para comparar! 

---
*Aviso: Los gráficos son curiosidad científica. ¡No los uses para apostar dinero real! El mercado es rudo.* 👨‍🔬🧠

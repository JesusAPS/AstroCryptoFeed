# 🤖 Astro-Bot - El Motor de Mi Laboratorio Cripto

¡Bienvenido al corazón de **AstroCryptoFeed**! Esta es la carpeta donde vive toda la lógica para conectarse con el mundo (APIs), agarrar la info y darle forma antes de guardarla. Aquí es donde ocurre la verdadera magia de Python y los inventos de un científico loco. 🧪✨

---

## 🧩 ¿Qué inventos hay aquí adentro?

*   **`bot.py`**: Es el cerebro principal. Se queda corriendo por siempre (dentro de Docker) llamando a todas las APIs sin cansarse.
*   **`utils/fetch_binance.py` y `fetch_coingecko.py`**: Son como los tentáculos que agarran los datos de afuera.
*   **`utils/analysis.py`**: **¡Aquí es donde Pandas brilla!** Calculo los indicadores técnicos para que el proyecto no sea un simple bot de precios, sino algo pro de análisis de mercado.
*   **`utils/database.py` y `save.py`**: Donde guardo todo en la base de datos SQLite para que no se pierda nada.

---

## 🏗️ Los Retos de un Científico Loco y Cómo los Vencí

### 1. El precio no lo es todo... 📉
Al principio mi bot solo avisaba si el Bitcoin caía, pero me di cuenta de que eso no servía de mucho sin contexto. Osea, le faltaba "condimento".
*   **Mi solución:** Le metí **Feature Engineering** usando la librería `ta`. Ahora extraigo el historial y calculo el **RSI (la fuerza)**, **Medias Móviles (para ver la tendencia)** y las **Bandas de Bollinger**. ¡Ahora sí tengo data de calidad! 💎

### 2. ¡El bot se me moría a cada rato! 💀
Si el internet fallaba o la API de Binance se ponía pesada, el script se cerraba y me dejaba sin datos a mitad de la noche. Un desastre total.
*   **Mi solución:** Lo hice súper resistente (resiliente, como dicen los cracks) usando bloques `try-except` en cada llamada. Ahora, si algo falla, mi **Logger (`utils/logger.py`)** anota qué pasó y el bot sigue adelante como si nada. ¡Nada lo detiene! 🛡️

### 3. El lío de organizar tanta data 🗃️
Con tantos indicadores, los archivos de texto eran un caos total. Necesitaba algo organizado de buena forma.
*   **Mi solución (`database.py`):** Usé **SQLAlchemy**. Esto me permite manejar mi base de datos SQLite como un profesional, sin escribir SQL crudo y manteniendo todo limpio y seguro. ¡Es una belleza!

---
*Hecho para aprender y experimentar. ¡No lo uses como bola de cristal para trading!* 👨‍🔬🧠

# 🤖 Astro-Bot - El Motor de Ingesta y Feature Engineering

¡Bienvenido al núcleo de **AstroCryptoFeed**! Esta carpeta contiene toda la lógica encargada de conectarse con el exterior (APIs), recolectar la información y cuadrarla antes de guardarla. Aquí es donde ocurre la verdadera magia de Python y el análisis técnico. ✨🛰️

---

## 📂 ¿Qué hay dentro del motor?

- `bot.py`: Es el cerebro principal. Se ejecuta infinitamente (dentro de Docker) orquestando las llamadas a las APIs.
- `utils/fetch_binance.py` y `fetch_coingecko.py`: Los conectores encargados de traer la data.
- `utils/analysis.py`: **¡Aquí es donde Pandas destaca!** Calculo los indicadores técnicos que hacen que este proyecto pase de ser un "bot que avisa precios" a una herramienta de análisis de mercado real. 📈
- `utils/database.py` y `save.py`: La persistencia hacia la base de datos (SQLite).

---

## 🏗️ Retos Técnicos y Cómo los Resolví

### 1. El precio solo no era suficiente... 📉
Al principio mi bot solo avisaba si el Bitcoin caía, pero me di cuenta de que eso no servía de mucho sin contexto.
*   **Mi solución:** Implementé **Feature Engineering** usando la librería `ta`. Ahora extraigo el historial y calculo el **RSI (Momentum)**, **Medias Móviles (SMA 20, EMA 20)** para ver la tendencia a corto y mediano plazo, y las **Bandas de Bollinger**. ¡Así quedó la data con mucho más valor! 💎

### 2. ¡El bot se caía si fallaba una API! 💀
Si el internet fallaba o la API de Binance daba error, el script se trancaba y me dejaba sin data a mitad de la noche. 
*   **Mi solución:** Hice el bot resiliente usando bloques de `try-except` envolviendo cada llamada. Ahora, si algo falla, mi **Logger (`utils/logger.py`)** registra el error ordenadamente y el bucle sigue vivo para el siguiente ciclo. ¡No se detiene por nada! 🛡️🚀

### 3. Gestionando los datos de forma escalable 🗃️
Con tantos indicadores, no podía seguir usando archivos de texto plano.
*   **Mi solución (`database.py`):** Configuré **SQLAlchemy**. Esta capa ORM me permitió definir la estructura clara de mis tablas y me olvidé de la sintaxis SQL cruda, organizando todo de forma impecable y segura. ✨🔨

---
*Hecho para aprender y experimentar con datos reales. Se recomienda usar solo con fines educativos.* 👨‍💻🛰️

# 🤖 Astro-Bot - El Motor de Ingesta y Feature Engineering

¡Bienvenido al núcleo de **AstroCryptoFeed**! Esta carpeta contiene toda la lógica encargada de conectarse con el mundo exterior (APIs), recolectar la información, y darle forma antes de guardarla. Aquí es donde ocurre la magia pura de Python y la "Ingeniería de Características" (Feature Engineering).

## 🧩 ¿Qué hay aquí adentro?

- `bot.py` - Es el "cerebro principal". Un script diseñado para ejecutarse infinitamente (dentro del contenedor Docker), orquestando las llamadas a las APIs.
- `utils/fetch_binance.py` y `fetch_coingecko.py` - Los conectores de APIs.
- `utils/analysis.py` - **¡Donde brilla Pandas!** Aquí calculo los indicadores técnicos que hacen que este proyecto pase de ser un "bot que avisa precios" a una herramienta de análisis de mercado.
- `utils/database.py` y `save.py` - La persistencia hacia la base de datos (SQLite).

---

## 🏗️ Los Problemas que Enfrenté y Cómo los Resolví

### Problema 1: "El precio actual no dice nada"
Mi primera versión del bot solo buscaba el precio de Bitcoin y si caía 5%, mandaba una alerta. **El problema:** ¡Los mercados son mucho más complejos! Un 5% de caída sin contexto no sirve.
✅ **Mi solución:** Implementé Feature Engineering avanzado usando la librería `ta` y extrayendo no solo el precio actual, sino la historia profunda (historcial Klines/Candlesticks). Ahora, antes de guardar el dato, le agrego valor calculando el **RSI (Momentum)**, **Medias Móviles (SMA 20, EMA 20)** para ver la tendencia a corto/mediano plazo, y las **Bandas de Bollinger** para entender la desviación de la volatilidad estadística en tiempo real.

### Problema 2: "El bot se muere cuando falla una API"
Al hacer llamadas a CoinGecko o Binance asíncronamente en un bucle `while True`, **el problema** principal es que de vez en cuando, el internet parpadea o el servidor de la API me rechaza (HTTP 429 Too Many Requests). Al principio, esto mataba mi script y dejaba de recolectar datos a las 2 AM.
✅ **Mi solución:** Hice el bot resiliente usando bloques robustos de `try-except` envolviendo cada llamada individual a las APIs. En lugar de un fallo catastrófico (Crash), ahora mi script utiliza un **Logger custom (`utils/logger.py`)** que registra el error ordenadamente (ej. `ERROR procesando CoinGecko: Timeout`) y el bucle sigue vivo para reintentarlo en el siguiente ciclo.

### Problema 3: "Gestión de Datos Escalable"
Con la cantidad masiva de indicadores (`rsi`, `sma`, etc.), no podía seguir usando archivos de texto.
✅ **Mi solución (`database.py`):** Configuré **SQLAlchemy**. Esta capa ORM me permitió definir la estructura clara de mis tablas (`class CryptoPrice`) y me olvidé de la sintaxis SQL cruda para la inserción, lo cual me previene de ataques de Inyección SQL y organiza todo maravillosamente. 

¡Espero que disfrutes leyendo este código tanto como yo disfruté optimizándolo!

---
*⚠️ **Recordatorio importante:** Este bot y sus cálculos son un ejercicio de programación. **No representan consejo financiero** ni una herramienta mágica para el trading. ¡Úsalo solo para aprender!*

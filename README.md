# 🪐 AstroCryptoFeed - Mi Proyecto de Datos Cripto

¡Hola! Bienvenido a **AstroCryptoFeed**. Este es un proyecto personal que nació de pura curiosidad por el mundo cripto y los datos. En esencia, es un pipeline automatizado que monitorea precios de criptomonedas (Binance y CoinGecko), los almacena, calcula indicadores financieros y los visualiza tanto en una web interactiva como en Power BI, llevándolo mucho más allá de una simple alerta de Telegram.

## 🧠 La Historia del Proyecto: Problemas y Soluciones

Cuando empecé este proyecto, mi idea original era muy simple: **quería un bot de Telegram que me avisara si el Bitcoin subía o bajaba mucho.** Pero a medida que fui armando todo, me di cuenta de que tenía frente a mí una oportunidad perfecta para aprender un montón de cosas y armar algo súper completo. Aquí te cuento cómo evolucionó y los retos que superé probando mis propias ideas:

### 1. El problema del almacenamiento (CSV vs Base de Datos)
Al principio, el bot guardaba los precios en archivos `.csv`. **El problema:** Rápidamente los CSV se volvieron pesados, difíciles de consultar y propensos a errores si el bot y el dashboard intentaban leer/escribir al mismo tiempo. 
✅ **Mi solución:** Migré toda la capa de persistencia a una base de datos **SQLite** usando SQLAlchemy. Esto me permitió abstraer la lógica, hacer consultas SQL estructuradas (`SELECT * FROM prices WHERE...`) y garantizar la integridad de los datos entre los distintos contenedores Docker.

### 2. Ver datos en la terminal vs verlo con gráficos
Tener un script en Python corriendo en la terminal es genial, pero después de un rato **el problema** es que me di cuenta de que sería mucho más divertido (y útil) analizarlos gráficamente.
✅ **Mi solución:** Construí un Dashboard interactivo usando **Streamlit**. Transformé un script en texto plano en una aplicación web con pestañas separadas para monitoreo en vivo y otra específicamente para bucear en el **Análisis Exploratorio de Datos (EDA)**.

### 3. Visualizaciones estáticas vs interactivas
Al crear el EDA, usé librerías básicas. **El problema:** Matplotlib generaba gráficos estáticos, poco atractivos y sin capacidad de hacer zoom en fechas precisas (algo vital en finanzas).
✅ **Mi solución:** Refactoricé toda la capa visual para usar **Plotly**. Ahora los gráficos de Velas Japonesas, Histogramas y Mapas de Calor de correlación son 100% interactivos y asombrosos.

### 4. Puente hacia Power BI
Sé que Pandas es genial y hace de todo, pero me dio curiosidad jugar también con **Power BI**. **El problema:** Calcular promedios móviles (SMA, EMA) y bandas de bollinger directamente con fórmulas en DAX es un dolor de cabeza y consume demasiados recursos mentalmente y técnicamente.
✅ **Mi solución:** Desarrollé un script ETL (`export_powerbi.py`) en Python que usa Pandas para precalcular todo el análisis técnico, lidiar con los valores nulos (`NaN`) y exportar un dataset plano (`.csv`) listo para ser devorado por Power BI en segundos.

---

## 📂 Arquitectura y Navegación

He dividido la documentación para que puedas entender cada pieza del rompecabezas. Te invito a leer los READMEs específicos en cada carpeta:

*   🤖 [`astro-bot/README.md`](astro-bot/README.md) - El motor de recolección de datos y Feature Engineering.
*   📊 [`dashboard/README.md`](dashboard/README.md) - La aplicación web Streamlit y la lógica de visualización (Plotly).
*   ⚙️ [`scripts/README.md`](scripts/README.md) - El pipeline de extracción ETL hacia Power BI.
*   ⚡ [`activepieces/README_AP.md`](activepieces/README_AP.md) - Configuración para orquestación de flujos (Webhooks).

## 🚀 Cómo Iniciar el Proyecto

1. **Clona y Configura**:
   ```bash
   cp .env.example .env
   ```
   *(Rellena tus credenciales de Binance y Telegram en el `.env`)*

2. **Levanta la Infraestructura (Docker)**:
   Empaqueté todo en contenedores para que no tengas problemas de dependencias en tu máquina. Construye y corre el proyecto en segundo plano con este comando:
   ```bash
   docker-compose up --build -d
   ```

3. **¡Pruébalo en tu Teléfono! (Telegram)**:
   - Abre Telegram y busca tu bot.
   - Escribe el comando `/start`.
   - Verás un menú interactivo con botones. Puedes tocar "Precio BTC" o usar comandos como `/precio SOLUSDT` y `/resumen`.
   - Si quieres ver lo que el bot está haciendo por detrás (logs), corre en tu consola:
     ```bash
     docker-compose logs -f astro-bot
     ```

4. **Explora los Datos Visualmente**:
   - Entra al Dashboard web en: `http://localhost:8501`
   - Si quieres jugar con Power BI, corre `python scripts/export_powerbi.py` y conecta Power BI Deskstop al archivo generado en `shared/data/powerbi_dataset.csv`.

¡Disfruta explorando el código!

---

## ⚠️ Aviso Legal / Disclaimer

**¡Atención!** Este proyecto es **puramente educativo y experimental**. 
* **NO es asesoramiento financiero (Not Financial Advice - NFA).** 
* **NO es una "fórmula mágica" para hacerse millonario.** 
* Las criptomonedas son activos extremadamente volátiles. Los indicadores técnicos que se calculan aquí (RSI, Medias Móviles, Bandas de Bollinger, etc.) representan modelos matemáticos sobre datos pasados y **nunca** garantizan resultados futuros.
* Úsalo bajo tu propio riesgo para aprender sobre datos, código e integraciones de software. ¡Juega seguro!

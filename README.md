# 🪐 AstroCryptoFeed - Ingesta de Datos y Análisis Técnico

¡Hola! Bienvenido a **AstroCryptoFeed**. Este proyecto nació de la curiosidad por el mundo cripto y las ganas de cuadrar un sistema de datos robusto. Lo que empezó como un simple bot de Telegram, terminó siendo un ecosistema completo donde conecto APIs de Binance y CoinGecko, guardo todo en SQL y analizo la data con gráficos interactivos y Power BI. 📊🚀

---

## 🚀 La Evolución del Proyecto: Retos y Soluciones

Aquí te cuento cómo fue que cuadré todo este sistema y los problemas que resolví mientras le daba forma a mi idea:

### 1. ¿Cómo guardo la data de forma eficiente? (De CSV a SQL) 💾
Al principio usé archivos `.csv`, pero eso se puso pesado rápido y se trancaba cuando el bot y el dashboard querían entrar al mismo tiempo.
*   **Mi solución:** Pasé toda la persistencia a **SQLite** usando SQLAlchemy. Ahora la data fluye de buena forma, todo está organizado con tablas y consultas SQL, y la integridad está garantizada. ✨

### 2. De ver solo texto a ver gráficos de verdad 📈
Tener un script en la consola está bien, pero yo quería ver la acción visualmente.
*   **Mi solución:** Monté un Dashboard interactivo con **Streamlit**. Así pude separar el monitoreo de los precios en vivo de la parte de **Análisis Exploratorio (EDA)** donde me pongo a chequear los historiales.

### 3. ¡Necesito interactividad total! (Plotly al rescate) 🕹️
Los gráficos básicos eran muy estáticos. No podía hacer zoom ni ver detalles de los puntos.
*   **Mi solución:** Refactoricé la parte visual para usar **Plotly**. Ahora tengo velas japonesas y mapas de calor que quedaron finos y son 100% interactivos. 🎯

### 4. Conectando con Power BI 👔
Siempre quise probar herramientas de BI, pero calcular indicadores técnicos (como RSI o EMA) dentro de Power BI con DAX es un proceso rudo y lento.
*   **Mi solución:** Hice un script ETL (`export_powerbi.py`) en Python que hace todo ese trabajo pesado. Calcula los indicadores, limpia los valores nulos y exporta un `.csv` listo para que Power BI lo consuma sin problemas. ⚡

---

## 📂 Arquitectura del Proyecto

He organizado todo por carpetas para que la navegación sea sencilla y clara:

| Carpeta | Descripción |
| :--- | :--- |
| 🤖 [`astro-bot/`](astro-bot/README.md) | El motor que extrae la data y calcula los indicadores técnicos. |
| 📊 [`dashboard/`](dashboard/README.md) | La aplicación web con Streamlit y los gráficos interactivos. |
| ⚙️ [`scripts/`](scripts/README.md) | El pipeline que prepara la data para Power BI. |
| ⚡ [`activepieces/`](activepieces/README_AP.md) | La automatización de flujos con webhooks y publicaciones. |

---

## 🛠️ Cómo Iniciar el Sistema

1.  **Configura tu ambiente**:
    Copia el archivo de ejemplo y pon tus credenciales:
    ```bash
    cp .env.example .env
    ```
2.  **Levanta todo con Docker**:
    Usa este comando para que los contenedores se encarguen de todo:
    ```bash
    docker-compose up --build -d
    ```
3.  **Chequea el Bot**:
    Busca tu bot en Telegram y dale `/start`. Puedes usar comandos como `/precio BTCUSDT` o ver el resumen con los botones.
4.  **Entra al Dashboard**:
    Abre `http://localhost:8501` en tu navegador para ver los gráficos en vivo.

---

## ⚠️ Nota Importante (Disclaimer)

Esta herramienta es **estrictamente educativa**.
*   **No es asesoría financiera.**
*   El mercado cripto es volátil y rudo. Usa estos datos solo para aprender sobre ingeniería de datos y análisis. ¡Sé responsable con tu dinero! 🖖

---
*Desarrollado con pasión por los datos y la tecnología.* 👨‍💻🛰️

# 🪐 AstroCryptoFeed - El Laboratorio Cripto de un Científico Loco 🚀

¡Epa! Bienvenido a **AstroCryptoFeed**. Este proyecto es básicamente el resultado de mi curiosidad infinita por los datos y las criptos. No es solo un bot de Telegram; es todo un experimento donde conecto APIs de Binance y CoinGecko, guardo todo en una base de datos y luego me pongo a inventar con gráficos interactivos y visualizaciones en Power BI. 🧪📊

---

## 🧠 La Locura Detrás del Proyecto: ¿Qué quise resolver?

Al principio solo quería que un bot me avisara si el Bitcoin subía, pero después me puse creativo (o loco, ajajaja) y terminé armando todo este ecosistema. Aquí te cuento los rollos que tuve y cómo los saqué adelante:

### 1. ¿Donde guardo tanta info? (Adiós CSV, hola SQL) 💾
Empecé guardando todo en archivos `.csv`, pero eso se puso súper pesado y se trababa cuando quería leer y escribir al mismo tiempo. 
*   **Mi solución:** Metí todo en una base de datos **SQLite** usando SQLAlchemy. Ahora todo fluye de buena forma, hago mis consultas SQL y los datos están seguros y organizados.

### 2. De ver texto plano a ver gráficos brutales 📈
Mirar la terminal es aburrido después de un rato, osea, necesitaba ver la acción en vivo. 
*   **Mi solución:** Monté un Dashboard con **Streamlit**. Separé una parte para ver los precios en tiempo real y otra especial para mi "Análisis Exploratorio de Datos" (EDA) donde me pongo a ver historiales.

### 3. ¡Quiero interactividad! (Plotly al rescate) 🕹️
Los gráficos de Matplotlib eran muy estáticos, no podía hacer zoom ni ver detalles. 
*   **Mi solución:** Cambié todo a **Plotly**. Ahora tengo velas japonesas y mapas de calor que se ven increíbles y son 100% interactivos. ¡Se ve demasiado pro!

### 4. El puente a Power BI 👔
Me dio por jugar con herramientas de BI, pero calcular cosas raras (como RSI o medias móviles) dentro de Power BI es un dolor de cabeza rudo.
*   **Mi solución:** Hice un script de Python (`export_powerbi.py`) que hace todo el trabajo sucio. Calcula los indicadores, limpia los nulos y me deja un regalito: un `.csv` perfecto listo para que Power BI lo devore sin esfuerzo.

---

## 📂 Mapa del Laboratorio (Arquitectura)

He organizado todo en carpetas para no volverme loco. Aquí puedes ver cada pieza:

| Carpeta | ¿Qué hay ahí? |
| :--- | :--- |
| 🤖 [`astro-bot/`](astro-bot/README.md) | Aquí vive el bot que extrae los datos y hace la magia técnica. |
| 📊 [`dashboard/`](dashboard/README.md) | La web con Streamlit y los gráficos interactivos de Plotly. |
| ⚙️ [`scripts/`](scripts/README.md) | El pipeline que prepara los datos para Power BI. |
| ⚡ [`activepieces/`](activepieces/README_AP.md) | La parte de automatización con webhooks (súper útil). |

---

## 🚀 Cómo poner a correr este monstruo

1.  **Configura tu ambiente**:
    Copia el archivo de ejemplo y pon tus llaves:
    ```bash
    cp .env.example .env
    ```
2.  **Dale vida con Docker**:
    Usa este comando para que todo se instale y corra solito:
    ```bash
    docker-compose up --build -d
    ```
3.  **Habla con el bot**:
    Busca tu bot en Telegram, dale `/start` y ¡listo! Toca los botones para ver el precio o usa `/precio BTCUSDT`.
4.  **Mira la web**:
    Entra a `http://localhost:8501` para ver el Dashboard.

---

## ⚠️ ¡Cuidado aquí! (Aviso Legal)

**¡Ojo!** Esto es puro experimento educativo. 
*   **NO es consejo financiero.** No me culpes si el mercado se vuelve loco, ajajaja.
*   Las criptos son volátiles de una forma ruda. Úsalo para aprender, no para apostar la casa. ¡Sé responsable! 🖖

---
*Hecho por un mini científico loco que ama los datos.* 👨‍🔬🧠

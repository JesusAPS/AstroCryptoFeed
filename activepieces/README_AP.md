# ⚡ Automatización con Activepieces

AstroCryptoFeed usa **Activepieces Cloud** como orquestador para generar y publicar contenido en Binance Square de forma semi-automática. Es una herramienta clave para mi flujo de trabajo. 🚀✨

---

## 🏗️ Cómo Orquesté el Flujo

```
⏰ Alarma (8:00, 16:00, 20:00 VET)
  → 📰 Lee Noticias: RSS de CoinTelegraph
    → 🤖 Google Gemini: Genera un post de calidad
      → 📱 Telegram: Envía el borrador al chat
        → ✅/🔄 Telegram: Botones de Aprobar o Reintentar
          → 🚀 HTTP POST: Webhook al bot en Render
            → 📢 Publicar: ¡Sale a Binance Square! 
```

---

## 🛠️ Herramientas Utilizadas

| Pieza | Función |
| :--- | :--- |
| `piece-schedule` | Mi disparador programado (Cron). |
| `piece-http` | Extrae el RSS y envía el webhook final. |
| `piece-google-gemini` | Genera el contenido con IA. |
| `piece-telegram-bot` | Notificaciones y flujo de aprobación. |

---

## 🧪 Descripción de los Pasos

1.  **Trigger (Cron):** Se activa a las 8 AM, 4 PM y 8 PM (Hora de Venezuela).
2.  **Extraer Noticias:** Uso un GET HTTP para sacar lo último de CoinTelegraph. 📰
3.  **Gemini al Ataque:** El modelo `gemini-2.5-flash` analiza la noticia y escribe un post de Binance Square con:
    *   Un gancho fuerte con emojis. 💥
    *   Cashtags obligatorios ($BTC, $ETH).
    *   Preguntas para que la gente comente.
    *   Hashtags pro: #Binance #CryptoNews.
4.  **Borrador a Telegram:** Me manda el texto para que yo lo vea.
5.  **Flujo de Aprobación:** Aparecen dos botones: **✅ Aprobar** o **🔄 Reintentar**. ¡Yo tengo el control total! 🕹️
6.  **Publicar:** Si apruebo, se envía un POST a Render y ¡listo! Publicado en Binance Square.

---

## ⚙️ Configuración en Render

Para que esto funcione en tu servidor, asegúrate de tener estas variables de entorno configuradas:

| Variable | Descripción |
| :--- | :--- |
| `BINANCE_SQUARE_API_KEY` | API Key de Binance Square OpenAPI (¡Expira cada 30 días!). |
| `BINANCE_API_KEY / SECRET` | Llaves generales de Binance. |
| `TELEGRAM_BOT_TOKEN / ID` | Datos de tu bot y chat de Telegram. |
| `ACTIVEPIECES_WEBHOOK_URL` | URL del webhook de flujo. |

---

## ⚙️ Mantenimiento

*   **API Key de Binance Square:** Renueva cada **25-30 días** en la configuración de OpenAPI de Binance Square. 
*   **Si recibes el error `220004`:** Significa que la llave expiró, genera una nueva y actualiza en Render. 
*   **Importar el flujo:** Puedes subir mi archivo `Automatizacion.json` directamente a Activepieces Cloud. ¡Solo recuerda reconectar tus llaves si aparecen en rojo! 🔴✨

---
*Diseñado por un apasionado de la automatización y los datos.* 👩‍🔬🛰️

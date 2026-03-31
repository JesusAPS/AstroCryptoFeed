# 🧩 El Lab de Automatización con Activepieces

AstroCryptoFeed se volvió súper inteligente con **Activepieces Cloud**. Aquí es donde orquesto todo de forma semiautomática para generar y publicar mi contenido en Binance Square sin volverme loco. ⚡🚀

---

## 🏗️ La Arquitectura de Mi Flujo (Mi Invento 🧪)

```
⏰ Alarma (8:00, 16:00, 20:00 VET)
  → 📰 Lee Noticias: RSS de CoinTelegraph
    → 🤖 Google Gemini: Crea un post de calidad
      → 📱 Telegram: Me manda el borrador
        → ✅/🔄 Yo decido: ¿Aprobar o Reintentar?
          → 🚀 Webhook: Envía la señal al bot en Render
            → 📢 Publicar: ¡Sale a Binance Square! 
```

---

## 🛠️ Piezas que usé en mi experimento

| Pieza | ¿Qué hace? |
| :--- | :--- |
| `piece-schedule` | Mi despertador personal (Cron). |
| `piece-http` | El que agarra las noticias y lanza el webhook. |
| `piece-google-gemini` | El cerebro de IA que escribe los posts. |
| `piece-telegram-bot` | Mi asistente que me avisa y me pide permiso. |

---

## 🧪 Los Pasos Detrás del Invento (Mi Lógica)

1.  **Trigger (Schedule):** Se activa a las 8 AM, 4 PM y 8 PM (hora de Venezuela).
2.  **Leer noticias:** Uso un GET HTTP para sacar lo último de CoinTelegraph. 📰
3.  **Gemini al ataque:** El modelo `gemini-2.5-flash` analiza la noticia y escribe un post de Binance Square con:
    *   Un gancho fuerte con emojis. 💥
    *   Cashtags obligatorios ($BTC, $ETH).
    *   Preguntas para que la gente comente.
    *   Hashtags pro: #Binance #CryptoNews.
4.  **Borrador a Telegram:** Me manda el texto para que yo lo vea.
5.  **Permiso de Científico Loco:** Aparecen dos botones: **✅ Aprobar** o **🔄 Reintentar**. ¡Yo tengo el control total! 🕹️
6.  **Publicar:** Si apruebo, se envía un POST a Render y ¡listo! Publicado en Binance Square.

---

## ⚙️ Lo que Necesitas Configurar en Render

Si quieres clonar mi invento, asegúrate de tener estas variables de entorno en Render:

| Variable | ¿Para qué es? |
| :--- | :--- |
| `BINANCE_SQUARE_API_KEY` | Mi llave de Binance Square (Ojo: ¡expira cada 30 días!). |
| `BINANCE_API_KEY / SECRET` | Mis llaves generales de Binance. |
| `TELEGRAM_BOT_TOKEN / ID` | Las llaves de mi bot y mi chat de Telegram. |
| `ACTIVEPIECES_WEBHOOK_URL` | La dirección del webhook de Activepieces. |

---

## 🧪 Mantenimiento de Mi Lab

*   **Renueva tu API Key de Binance Square:** Hazlo cada **25-30 días** en la configuración de OpenAPI de Binance Square. Si te sale el error `220004`, ¡es porque se venció! Genera una nueva y cámbiala en Render. 
*   **Importar el flujo:** Puedes subir mi archivo `Automatizacion.json` directamente a Activepieces Cloud. ¡Solo recuerda reconectar tus llaves (Gemini y Telegram) si aparecen en rojo! 🔴✨

---
*Hecho por un mini científico loco que ama automatizarlo todo.* 👨‍🔬🤖

# 🧩 Guía de Integración con Activepieces

AstroCryptoFeed usa **Activepieces Cloud** como orquestador de automatización para generar y publicar contenido en Binance Square de forma semi-automática.

## Arquitectura del Flujo

```
⏰ Schedule (8:00, 16:00, 20:00 VET)
  → 📰 HTTP GET: RSS de CoinTelegraph
    → 🤖 Google Gemini: Genera post optimizado
      → 📱 Telegram: Envía borrador al chat
        → ✅/🔄 Telegram: Botones de Aprobar/Rechazar
          → 🚀 HTTP POST: Webhook al bot en Render
            → 📢 Bot: Publica en Binance Square via OpenAPI
```

## Piezas Utilizadas

| Pieza | Versión | Función |
|-------|---------|---------|
| `@activepieces/piece-schedule` | ~0.1.17 | Trigger programado (cron) |
| `@activepieces/piece-http` | ~0.11.7 | Extraer RSS y enviar webhook |
| `@activepieces/piece-google-gemini` | ~0.1.4 | Generar contenido con IA |
| `@activepieces/piece-telegram-bot` | ~0.5.6 | Notificaciones y aprobación |

## Descripción de Cada Paso

### 1. Trigger — Schedule (Cron)
- **Horarios:** `0 8,16,20 * * *` (8:00 AM, 4:00 PM, 8:00 PM)
- **Zona horaria:** `America/Caracas`

### 2. step_2 — Extraer Noticias (HTTP GET)
- **URL:** `https://cointelegraph.com/rss`
- **Método:** GET
- **Salida:** XML/RSS con las últimas noticias cripto

### 3. step_1 — Generar Contenido (Google Gemini)
- **Modelo:** `gemini-2.5-flash`
- **Prompt:** Estratega de contenido de Binance Square que analiza noticias de CoinTelegraph
- **Reglas del prompt:**
  - Gancho con emojis en MAYÚSCULAS
  - Máximo 2 frases en el cuerpo
  - Cashtag obligatorio ($BTC, $ETH, $BNB, etc.)
  - Pregunta abierta para interacción
  - Hashtags: #Binance #CryptoNews + 1 específico
  - **TEXTO PLANO** (sin Markdown)
  - Máximo 1000 caracteres

### 4. step_4 — Enviar Borrador a Telegram
- **Acción:** `send_text_message`
- **Formato:** HTML
- **Chat ID:** `1540989235`
- Envía el texto generado por Gemini para revisión

### 5. step_3 — Solicitar Aprobación (Telegram)
- **Acción:** `request_approval_message`
- **Botón Aprobar:** `✅ Aprobar`
- **Botón Rechazar:** `🔄 Generar otro (Reintentar)`

### 6. step_5 — Router (Decisión)
- **Condición:** `step_3['approved'] == True` (case insensitive)
- **Branch 1 (Aprobado):** Ejecuta step_6 (publicar)
- **Branch 2 (Rechazado):** Ejecuta step_7 (mensaje de rechazo)

### 7. step_6 — Publicar en Binance Square (HTTP POST)
- **URL:** `https://astrocryptofeed.onrender.com/webhook/publish`
- **Método:** POST
- **Headers:** `Content-Type: application/json`
- **Body:** `{ "content": "{{step_1}}" }`
- El bot en Render recibe el texto y usa la API de Binance Square con el header `X-Square-OpenAPI-Key`

### 8. step_7 — Mensaje de Rechazo (Telegram)
- Envía un mensaje informando que el post fue descartado

## Variables de Entorno Requeridas en Render

| Variable | Descripción |
|----------|-------------|
| `BINANCE_SQUARE_API_KEY` | API Key de Binance Square OpenAPI (expira cada ~30 días) |
| `BINANCE_API_KEY` | API Key general de Binance |
| `BINANCE_API_SECRET` | API Secret de Binance |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram |
| `TELEGRAM_CHAT_ID` | ID del chat de Telegram |
| `ACTIVEPIECES_WEBHOOK_URL` | URL del webhook de Activepieces |

## Conexiones en Activepieces

- **Google Gemini:** API Key de Google AI Studio (conexión `XpbRUZyVktwSfr6qeWKNn`)
- **Telegram Bot:** Token del bot (conexión `sjGWK712zYSoAEwnMITeL`)

> ⚠️ **Nota:** Después de importar `Automatizacion.json`, verifica que las conexiones estén activas. Si aparecen en rojo, re-selecciona las credenciales.

## Importar el Flujo

1. Ve a **Activepieces Cloud** → Tu proyecto
2. Clic en `...` → **Import Flow**
3. Selecciona `activepieces/Automatizacion.json`
4. Verifica las conexiones (Gemini y Telegram)
5. Publica el flujo

## Mantenimiento

- **API Key de Binance Square:** Renueva cada **25-30 días** en Binance → Square → OpenAPI Settings
- **Si recibes error `220004`:** La API Key expiró, genera una nueva y actualiza en Render
- **Si recibes error `220003`:** Verifica el nombre de la variable en Render (`BINANCE_SQUARE_API_KEY`)

# 🧩 Guía de Integración con Activepieces

AstroCryptoFeed ahora envía eventos y alertas a Activepieces. Activepieces es una alternativa moderna y ligera a herramientas como Zapier o n8n.

## 1. Configurar tu Webhook en Activepieces

1. Inicia sesión en tu instancia de Activepieces (por defecto disponible en `http://localhost:8080`).
2. Crea una **Nueva Colección/Flujo (New Flow)**.
3. Para el **Trigger (Disparador)** inicial, selecciona **Webhook**.
4. Elige **Catch Webhook**.
5. Activa tu flujo para generar una **Test URL**.
6. Copia esa **Test URL**.

## 2. Configurar AstrosCryptoFeed

1. Abre el archivo `.env` del proyecto.
2. Pega la URL que copiaste en la variable `ACTIVEPIECES_WEBHOOK_URL`:
   ```env
   ACTIVEPIECES_WEBHOOK_URL=http://localhost:8080/api/v1/webhooks/TU_ID_AQUI
   ```

## 3. Probar la Conexión

1. Vuelve a Activepieces y haz clic en **Test Trigger**.
2. Espera a que `astro-bot` encuentre una alerta, o fuerza una cambiando la variable `ALERT_PERCENT` a un valor muy bajo (ej: `0.1`) en el `.env` y reinicia el contenedor del bot (`docker-compose restart astro-bot`).
3. Verás que Activepieces recibe de inmediato un JSON con este formato:

   ```json
   {
     "asset": "BTCUSDT",
     "price": 45000.50,
     "change_24h": 5.2,
     "rsi": 35.5,
     "signal": "NEUTRAL",
     "source": "Binance"
   }
   ```

## 4. Conectar Gemini con Activepieces (Generación de Contenido)

Activepieces incluye una pieza nativa para **Google Gemini**. Puedes usarlo para analizar las alertas de AstroCryptoFeed o noticias de un RSS y generar posts atractivos.

1.  **Añade la pieza de Gemini** después de tu Webhook (o pieza RSS).
2.  **Configura la Conexión**:
    *   Si usas Google AI Studio (Gratis): Pega tu API Key de Gemini aquí.
    *   Si usas Google Cloud (Pro): Configura la API Key vinculada a tu proyecto.
3.  **Prompt Maestro**: He creado un archivo específico con el prompt maestro: [`prompt_maestro_binance_square.txt`](prompt_maestro_binance_square.txt).
    Cópialo y pégalo en el paso de Gemini. Reemplaza las variables `{{trigger.title}}` y `{{trigger.description}}` con los datos de tu pieza de RSS (o los datos del Webhook si prefieres).

*💡 Tip Pro:* Pasa los datos de SQLite o los JSON del bot (ej: `Precio de BTC: $95,000, RSI en 70`) a este prompt en lugar de (o junto con) simples noticias RSS para que la IA haga análisis técnico en tiempo real.

## 5. El Flujo Maestro (Configuración Real)

Basado en la configuración actual (`Automatizacion.json`), el flujo trabaja así:

1.  **Gatillo (Trigger):** Pieza de **Schedule** (Programación). Configurado para las **8:00, 16:00 y 20:00** (Hora de Caracas).
2.  **Extracción de Noticias:** Pieza de **HTTP** que consulta el RSS de `cointelegraph.com/rss`.
3.  **Cerebro (IA):** Pieza de **Google Gemini** redacta el post optimizado usando el **Prompt Maestro**.
4.  **Notificación de Filtro:** Pieza de **Telegram** te envía el borrador para que lo leas.
5.  **Solicitud de Aprobación:** Pieza de **Telegram (Request Approval)** que muestra dos botones en tu chat:
    *   `✅ Aprobar`: Envía el contenido a publicar.
    *   `🔄 Generar otro (Reintentar)`: Descarta el post actual.
6.  **Publicación Técnica (Router):** 
    *   Si pulsas **Aprobar**, Activepieces hace un `POST` a tu bot en Render: `https://astrocryptofeed.onrender.com/webhook/publish`.
    *   Tu bot recibe el texto y usa la **API Oficial de Binance Square** para publicar.

### 📦 Configuración del Payload (Paso Crítico)
En el paso final de **HTTP (POST)**, la configuración debe ser:
- **URL:** `https://astrocryptofeed.onrender.com/webhook/publish`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
  ```json
  {
    "content": "{{step_1.output}}" 
  }
  ```
  *(Asegúrate de que `step_1` sea el resultado del paso de Gemini).*

*Nota: Hemos pasado de la publicación manual a un sistema de **"Un solo clic"** desde Telegram.*

## 6. Siguientes Pasos (Otras Acciones)
Si no usas Binance Square, recuerda que también puedes conectar herramientas como:
*   **Discord / Slack**: Para notificaciones enriquecidas.
*   **Google Sheets**: Para crear un registro histórico en una hoja de cálculo.

¡Disfruta automatizando! 🚀

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

## 5. Publicación y Aprobación por Telegram (El Flujo Elegido)

Para mantener el control y asegurar la calidad, usaremos el sistema de **Aprobación Humana vía Telegram** antes de publicar en Binance Square.

El flujo sugerido en Activepieces es:
1.  **Gatillo (Trigger):** Pieza de **RSS** (Blog de Binance) o Webhook de Astro-Bot.
2.  **IA:** Pieza de **Gemini** lee la noticia y genera el borrador.
3.  **Acción (Telegram):** La pieza de **Telegram** te envía el borrador para aprobación.

### 📦 Configuración del Mensaje de Telegram
Configura el campo de "Text" en tu pieza de Telegram exactamente así:

```text
📦 NUEVO POST PARA BINANCE SQUARE

Contenido sugerido por Gemini:
{{step_de_gemini.output}}

🔗 Noticia original: {{trigger.link}}
```

4.  **Aprobación/Publicación:** Lees el mensaje de Telegram, lo copias y lo publicas manualmente en Binance Square.

*(Decidimos no usar la Opción A - Publicación Directa automática para siempre revisar lo que la IA escriba primero).*

## 6. Siguientes Pasos (Otras Acciones)
Si no usas Binance Square, recuerda que también puedes conectar herramientas como:
*   **Discord / Slack**: Para notificaciones enriquecidas.
*   **Google Sheets**: Para crear un registro histórico en una hoja de cálculo.

¡Disfruta automatizando! 🚀

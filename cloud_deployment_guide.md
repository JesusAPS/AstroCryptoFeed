# Despliegue en la Nube (Opción B - 100% Gratis)

Esta guía te explicará cómo alojar tu bot de Python (`AstroCryptoFeed`) de forma gratuita para que funcione 24/7 sin depender de tu computadora encendida.

Usaremos dos servicios en la nube gratuitos:
1.  **Activepieces Cloud:** Para alojar el flujo visual y Gemini.
2.  **Render.com:** Para alojar tu código de Python (el recolector de noticias y conectores a Telegram).

---

## ☁️ Paso 1: Configurar Activepieces Cloud (Avanzado)

1. Ve a [Cloud Activepieces](https://cloud.activepieces.com/) y crea una cuenta gratuita.
2. Crea un **Nuevo Flujo** (New Flow) y nómbralo "Publicación Programada Binance Square".
3. **Trigger (Disparador):** Selecciona **Schedule** (Cron).
   - Configúralo para que se active 3 veces al día: `08:00`, `16:00` y `20:00`.
4. **Acción 1 (RSS):** Agrega la pieza RSS para leer el Blog de Binance (u otra fuente).
5. **Acción 2 (Gemini):** Agrega Gemini y pega el **Prompt Maestro** que editamos antes.
6. **Acción 3 (Aprobación Interactiva):**
   - Agrega la pieza **"Approval"** (o busca "Manage Approvals").
   - Configura que envíe la notificación por **Telegram**.
   - **Botones:** Configura dos botones: 
     - 🟢 **"Publicar"**: Si lo presionas, Activepieces continúa a la acción de subir a Binance Square.
     - ✍️ **"Modificar"**: Si lo presionas, envías una instrucción de vuelta a Gemini para que genere una versión distinta.
7. **Paso Final (Opcional):** Conecta la API de Binance Square con tus nuevas claves para que la publicación se haga sola al presionar "Publicar".
8. ¡Dale a **Publish** en la web de Activepieces!

---

## 🔄 Paso 2: Subir tu código a GitHub

Render necesita que tu código esté en internet para poder descargarlo y ejecutarlo. La mejor forma de hacerlo es usando GitHub.

1. Si no tienes cuenta, regístrate en [GitHub.com](https://github.com/).
2. Crea un nuevo repositorio (privado o público).
3. Sube todos los archivos de tu proyecto `AstroCryptoFeed` a ese repositorio.
   *(Nota: Asegúrate de **NO** subir el archivo `.env` con tus contraseñas reales. Sube solo el código y el `.env.example`)*.

---

## 🚀 Paso 3: Desplegar el Bot en Render

1. Crea una cuenta gratuita en [Render.com](https://render.com/). Puedes usar tu misma cuenta de GitHub para iniciar sesión.
2. Haz clic en **"New"** (Nuevo) y selecciona **"Web Service"** (Servicio Web).
   *(Aunque es un bot, lo configuramos como "Web Service" gracias al pequeño servidor integrado que le pusimos, así Render no lo apaga)*.
3. Conecta tu cuenta de GitHub y selecciona el repositorio que creaste en el Paso 2.
4. Completa la configuración del servicio:
   - **Name:** `astro-crypto-bot` (o el nombre que quieras).
   - **Environment:** `Python 3`
   - **Region:** Selecciona la más cercana (ej. `US East` o `Frankfurt`).
   - **Branch:** `main` (o `master`).
   - **Build Command:** `pip install -r astro-bot/requirements.txt`
   - **Start Command:** `cd astro-bot && python bot.py`
5. Selecciona el plan **Free** ($0/month).
6. **MUY IMPORTANTE:** Ve a la sección de **"Environment Variables"** (Variables de Entorno) en Render y dales click a "Add Environment Variable". Debes pegar **todas las variables** de tu archivo `.env` manual una por una. (Ejem: `BINANCE_API_KEY`, `TELEGRAM_BOT_TOKEN`, `ACTIVEPIECES_WEBHOOK_URL`).
7. Finalmente, haz clic en **"Create Web Service"**.

¡Listo! Render descargará tu código, instalará las librerías necesarias y ejecutará tu bot. En la pestaña "Logs" de Render podrás ver cómo cobra vida.

---

## ⏰ Paso 4: Evitar que el Bot se "duerma"

Los servicios gratuitos de Render se "duermen" (hibernan) si no reciben tráfico web durante 15 minutos. Para evitar esto:
1. Copia la URL pública que Render te dará para tu Web Service (arriba a la izquierda, termina en `.onrender.com`).
2. Ve a [UptimeRobot](https://uptimerobot.com/) (es gratis).
3. Crea un nuevo "Monitor" de tipo HTTP(s).
4. Pega la URL de tu app en Render.
5. Configúralo para que envíe un "Ping" cada 10 minutos.

De esta forma, UptimeRobot "tocará la puerta" de tu bot cada 10 minutos, asegurándose de que Render lo mantenga encendido 24/7 sin cobrarte nada.

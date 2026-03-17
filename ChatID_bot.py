import os
from telegram import Update
# Libreria para enviar mensajes a Telegram
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Token del bot para prueba y obtener el chat ID
Telegram_Token = os.getenv('TELEGRAM_BOT_TOKEN')  # ← Token del bot

# Función para enviar mensaje de bienvenida y obtener el chat ID
async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "astronauta"
    
    mensaje = (
        f"👋 ¡Hola {user_name}!\n\n"
        f"🪐 Bienvenido a *JesusAPS Automatic*, tu centro de comando para automatización y alertas inteligentes.\n"
        f"🚀 Este bot está en fase de prueba, pero ya está orbitando con fuerza.\n\n"
        f"🛰️ Tu Chat ID es: `{chat_id}`\n"
        f"📡 Pronto recibirás señales cósmicas con precios, datos y herramientas útiles.\n\n"
        f"_Gracias por ser parte de esta misión espacial._ 🌌"
    )
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")

app = ApplicationBuilder().token(Telegram_Token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome_message))
app.run_polling()


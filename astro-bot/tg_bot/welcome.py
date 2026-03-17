from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config.settings import TELEGRAM_BOT_TOKEN

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

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome_message))
app.run_polling()

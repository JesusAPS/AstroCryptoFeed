import asyncio
import os
import requests
import json
from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.format import log_event

ACTIVEPIECES_WEBHOOK_URL = os.getenv("ACTIVEPIECES_WEBHOOK_URL")

async def send_telegram_alert_async(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        log_event("Alerta Telegram enviada", "success")
    except Exception as e:
        log_event(f"Error enviando alerta Telegram: {e}", "error")

def send_telegram_alert(message: str):
    asyncio.run(send_telegram_alert_async(message))

def send_activepieces_webhook(data: dict):
    """Envía los datos de la alerta a Activepieces."""
    if not ACTIVEPIECES_WEBHOOK_URL:
        return

    try:
        response = requests.post(ACTIVEPIECES_WEBHOOK_URL, json=data, timeout=5)
        if response.status_code == 200:
            log_event("Webhook Activepieces enviado", "success")
        else:
            log_event(f"Error Activepieces: {response.status_code}", "error")
    except Exception as e:
        log_event(f"Error conectando con Activepieces: {e}", "error")

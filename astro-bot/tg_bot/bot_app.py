import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from config.settings import TELEGRAM_BOT_TOKEN
from utils.fetch_binance import get_binance_data
from utils.database import get_engine
import pandas as pd

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje con el menú interactivo cuando se usa /start."""
    user_name = update.effective_user.first_name or "Astronauta"
    
    keyboard = [
        [
            InlineKeyboardButton("📈 Precio BTC", callback_data='price_BTCUSDT'),
            InlineKeyboardButton("📈 Precio ETH", callback_data='price_ETHUSDT')
        ],
        [
            InlineKeyboardButton("📈 Precio BNB", callback_data='price_BNBUSDT'),
            InlineKeyboardButton("📈 Precio SOL", callback_data='price_SOLUSDT')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🌌 ¡Hola {user_name}! Bienvenido al panel de control interactivo de **AstroCryptoFeed**.\n\n"
        "Soy tu asistente de trading y análisis de datos. ¿Qué deseas hacer hoy?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Obtiene el precio de una moneda específica mediante comando (ej. /precio BTCUSDT)."""
    if not context.args:
        await update.message.reply_text("⚠️ Por favor, indica el par. Ejemplo: `/precio BTCUSDT`", parse_mode='Markdown')
        return
        
    symbol = context.args[0].upper()
    data = get_binance_data(symbol)
    
    if data:
        msg = (
            f"💹 *{data['symbol']}*\n"
            f"Precio: `${data['price']:.2f}`\n"
            f"Cambio 24h: `{data['change']:.2f}%`"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No encontré datos para ese par o hay un error de conexión.")

async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra un resumen de las monedas con mayor volatilidad hoy desde SQLite."""
    try:
        engine = get_engine()
        query = "SELECT symbol, change_24h FROM prices GROUP BY symbol ORDER BY timestamp DESC LIMIT 10"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            await update.message.reply_text("Todavía no he recolectado suficientes datos en mi base de datos.")
            return
            
        # Limpiar duplicados guardando el registro más reciente por moneda
        df = df.drop_duplicates(subset=['symbol'])
        # Ordenar por el mayor cambio absoluto (volatilidad)
        df['abs_change'] = df['change_24h'].abs()
        df = df.sort_values(by='abs_change', ascending=False).head(3)
        
        msg = "🌪 *Snapshot de Mayor Volatilidad Hoy:*\n\n"
        for _, row in df.iterrows():
            emoji = "📈" if row['change_24h'] > 0 else "📉"
            msg += f"• `{row['symbol']}`: {row['change_24h']:.2f}% {emoji}\n"
            
        await update.message.reply_text(msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error en /resumen: {e}")
        await update.message.reply_text("Error calculando el resumen estadístico.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los clicks en los botones interactivos."""
    query = update.callback_query
    await query.answer() # Vital para que telegram sepa que recibimos el click
    
    data = query.data
    if data.startswith("price_"):
        symbol = data.split("_")[1]
        market_data = get_binance_data(symbol)
        if market_data:
            msg = (
                f"💹 *{market_data['symbol']}*\n"
                f"Precio: `${market_data['price']:.2f}`\n"
                f"Cambio 24h: `{market_data['change']:.2f}%`"
            )
            await query.edit_message_text(text=msg, parse_mode='Markdown')
        else:
            await query.edit_message_text(text="Error obteniendo el precio en este momento.")

async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra estadísticas semanales: top monedas más volátiles de los últimos 7 días."""
    try:
        engine = get_engine()
        query_sql = """
            SELECT symbol, 
                   MIN(price) as min_price, 
                   MAX(price) as max_price,
                   AVG(change_24h) as avg_change,
                   MAX(ABS(change_24h)) as max_volatility,
                   COUNT(*) as data_points
            FROM prices 
            WHERE timestamp >= datetime('now', '-7 days')
              AND source = 'Binance'
            GROUP BY symbol 
            ORDER BY max_volatility DESC 
            LIMIT 5
        """
        df = pd.read_sql(query_sql, engine)
        
        if df.empty:
            await update.message.reply_text("No hay suficientes datos de la última semana aún.")
            return
        
        msg = "📊 *Resumen Semanal — Top 5 Volátiles:*\n\n"
        for _, row in df.iterrows():
            emoji = "🔥" if row['max_volatility'] > 5 else "📈"
            price_range = f"${row['min_price']:.2f} - ${row['max_price']:.2f}"
            msg += (
                f"{emoji} `{row['symbol']}`\n"
                f"   Rango: {price_range}\n"
                f"   Mayor movimiento: `{row['max_volatility']:.2f}%`\n"
                f"   Datos: {int(row['data_points'])} lecturas\n\n"
            )
        
        msg += "_Período: últimos 7 días_"
        await update.message.reply_text(msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error en /semana: {e}")
        await update.message.reply_text("Error calculando las estadísticas semanales.")

def create_bot_app():
    """Construye y devuelve la aplicación de telegram lista para correr."""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("No hay TELEGRAM_BOT_TOKEN configurado. El bot interactivo no se iniciará.")
        return None
        
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Comandos que aparecen en el menú "Menú" de Telegram
    commands = [
        ("start", "Iniciar el panel de control"),
        ("precio", "Ver precio de un par (Ej: /precio BTCUSDT)"),
        ("resumen", "Top 3 monedas con mayor movimiento hoy"),
        ("semana", "Estadísticas de volatilidad semanal")
    ]
    # No los seteamos aquí directamente porque es asíncrono, 
    # pero el usuario los puede ver en el código o los registramos en el bot.py
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("precio", price_command))
    app.add_handler(CommandHandler("resumen", resume_command))
    app.add_handler(CommandHandler("semana", week_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    return app


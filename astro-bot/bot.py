import asyncio
import os
import time
from utils.fetch_binance import get_binance_data, get_historical_klines
from utils.fetch_coingecko import get_coingecko_data
from utils.save import save_data
from utils.notify import send_telegram_alert, send_activepieces_webhook
from utils.api_key_monitor import check_api_key_expiry
from utils.logger import setup_logger
from utils.analysis import calculate_technical_indicators, get_signal
from utils.database import init_db
from utils.fetch_sentiment import get_fear_and_greed, get_binance_long_short_ratio
from utils.binance_square import publish_to_binance_square
from utils.format import get_crypto_tags
from tg_bot.bot_app import create_bot_app
import nest_asyncio
from aiohttp import web

# Soporte para event loops anidados si se corre en entornos especiales
nest_asyncio.apply()

# Configuración Multi-Par
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))
ALERT_PERCENT = float(os.getenv('ALERT_PERCENT', 5.0))

# Parsear listas de variables de entorno
BINANCE_PAIRS = os.getenv('BINANCE_PAIRS', 'BTCUSDT').split(',')
COINGECKO_IDS = os.getenv('COINGECKO_IDS', 'bitcoin').split(',')

# Rastreador de últimas alertas para evitar spam (Diccionario: {simbolo: timestamp})
last_alerts = {}
ALERT_COOLDOWN_SECONDS = 3600  # 1 hora de espera entre alertas del mismo par

logger = setup_logger()

def format_alert_message(name, price, change, source, rsi=None, signal="NEUTRAL", fear_greed=None, ls_ratio=None):
    arrow = "📈" if change > 0 else "📉"
    
    msg = (
        f"*🚨 ALERTA DE PRECIO*\n"
        f"*Activo:* `{name}`\n"
        f"*Precio actual:* `${price:.2f}`\n"
        f"*Cambio 24h:* `{change:.2f}%` {arrow}\n"
    )
    
    if rsi is not None:
        msg += f"*RSI (14):* `{rsi:.2f}`\n"
        msg += f"*Señal Técnica:* {signal}\n"

    if fear_greed is not None:
        msg += f"*Índice Miedo/Codicia:* `{fear_greed}`\n"

    if ls_ratio is not None:
        msg += f"*Ratio Long/Short:* `{ls_ratio:.2f}`\n"
        
    cashtag, hashtags = get_crypto_tags(name)
    msg += f"\n{cashtag} {hashtags}\n"
    msg += f"_Fuente: {source}_"
    return msg

async def data_collection_loop():
    """Bucle infinito que extrae, analiza y guarda datos de las APIs."""
    logger.info("📡 Iniciando subproceso de recolección de datos...")
    
    while True:
        try:
            # --- BINANCE (Iterar pares) ---
            for symbol in BINANCE_PAIRS:
                symbol = symbol.strip()
                try:
                    binance_data = get_binance_data(symbol)
                    klines_df = get_historical_klines(symbol, limit=100)
                    
                    if binance_data and not klines_df.empty:
                        # Análisis Técnico
                        indicators_df = calculate_technical_indicators(klines_df)
                        current_rsi = indicators_df['rsi'].iloc[-1]
                        signal_text, signal_emoji = get_signal(current_rsi)
                        full_signal = f"{signal_emoji} {signal_text}"

                        # --- ENRIQUECIMIENTO ---
                        sentiment = get_fear_and_greed()
                        ls_ratio = get_binance_long_short_ratio(symbol)
                        
                        fng_value = sentiment['value'] if sentiment else None
                        fng_text = sentiment['sentiment'] if sentiment else "Desconocido"
                        ls_val = ls_ratio['long_short_ratio'] if ls_ratio else None

                        # Guardar
                        binance_data['rsi'] = current_rsi
                        binance_data['fear_greed'] = fng_value
                        binance_data['long_short_ratio'] = ls_val
                        save_data(binance_data)

                        # Alertas
                        is_price_alert = abs(binance_data['change']) >= ALERT_PERCENT
                        is_technical_alert = "SOBRE" in signal_text
                        is_extreme_rsi = current_rsi < 30 or current_rsi > 70

                        if is_price_alert or is_technical_alert:
                            current_time = time.time()
                            last_alert_time = last_alerts.get(symbol, 0)
                            
                            # Verificar si pasó el tiempo de enfriamiento (cooldown)
                            if current_time - last_alert_time >= ALERT_COOLDOWN_SECONDS:
                                msg = format_alert_message(
                                    binance_data['symbol'], 
                                    binance_data['price'], 
                                    binance_data['change'], 
                                    "Binance",
                                    rsi=current_rsi,
                                    signal=full_signal,
                                    fear_greed=fng_value,
                                    ls_ratio=ls_val
                                )
                                # Telegram (Enviado de forma sincrona para esta iteración)
                                send_telegram_alert(msg)
                                logger.info(f"Alerta enviada para {symbol}")
                                
                                # Registrar el tiempo de esta alerta
                                last_alerts[symbol] = current_time

                                # Activepieces Webhook
                                cashtag, hashtags = get_crypto_tags(symbol)
                                webhook_data = {
                                    "asset": symbol,
                                    "cashtag": cashtag,
                                    "hashtags": hashtags,
                                    "price": binance_data['price'],
                                    "change_24h": binance_data['change'],
                                    "rsi": current_rsi,
                                    "fear_greed_index": fng_value,
                                    "fear_greed_sentiment": fng_text,
                                    "long_short_ratio": ls_val,
                                    "signal": signal_text,
                                    "source": "Binance"
                                }
                                send_activepieces_webhook(webhook_data)
                            else:
                                logger.info(f"Silenciando alerta repetida para {symbol} (Enfriamiento)")
                except Exception as e:
                    logger.error(f"Error procesando {symbol}: {e}")
                
            # --- COINGECKO (Iterar IDs) ---
            for token_id in COINGECKO_IDS:
                token_id = token_id.strip()
                try:
                    coingecko_data = get_coingecko_data(token_id)
                    if coingecko_data:
                        save_data(coingecko_data)
                        if abs(coingecko_data['change']) >= ALERT_PERCENT:
                            current_time = time.time()
                            last_alert_time = last_alerts.get(token_id, 0)
                            
                            if current_time - last_alert_time >= ALERT_COOLDOWN_SECONDS:
                                msg = format_alert_message(coingecko_data['token'], coingecko_data['price'], coingecko_data['change'], "CoinGecko")
                                send_telegram_alert(msg)
                                logger.info(f"Alerta enviada para {token_id} (CG)")
                                last_alerts[token_id] = current_time
                                
                                # Activepieces Webhook
                                cashtag, hashtags = get_crypto_tags(token_id)
                                webhook_data = {
                                    "asset": token_id,
                                    "cashtag": cashtag,
                                    "hashtags": hashtags,
                                    "price": coingecko_data['price'],
                                    "change_24h": coingecko_data['change'],
                                    "source": "CoinGecko"
                                }
                                send_activepieces_webhook(webhook_data)
                            else:
                                logger.info(f"Silenciando alerta repetida para {token_id} (Enfriamiento CG)")
                except Exception as e:
                    logger.error(f"Error procesando {token_id}: {e}")

        except Exception as e:
            logger.error(f"Error en el ciclo principal de datos: {e}")
        
        # Usar asyncio.sleep en lugar de time.sleep para no bloquear el Hilo principal
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    """Punto de entrada asíncrono que orquesta la recolección de datos y el Bot Interactivo."""
    init_db() # Crear tablas si no existen
    logger.info("🚀 Astro-Bot iniciado")
    logger.info(f"Configuración: {len(BINANCE_PAIRS)} pares en Binance y {len(COINGECKO_IDS)} en CoinGecko")
    
    # Verificar expiración de API Key de Binance Square
    check_api_key_expiry()
    
    # Iniciar la aplicación de Telegram interactiva
    app = create_bot_app()
    if app:
        logger.info("🤖 Bot de Telegram Interactivo preparado.")
        # Iniciamos el servidor de telegram en background
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    # --- INICIO DEL SERVIDOR WEB DUMMY PARA RENDER ---
    # Render exige que los "Web Services" escuchen en un puerto HTTP para saber que están vivos.
    async def handle_ping(request):
        return web.Response(text="AstroCryptoFeed Bot is alive and running!")
        
    async def handle_publish_webhook(request):
        """Webhook para recibir órdenes de publicar desde Activepieces."""
        try:
            data = await request.json()
            content = data.get('content', '')
            
            if not content:
                return web.json_response({'status': 'error', 'message': 'No content provided'}, status=400)
            
            logger.info("Recibida orden de publicar desde Activepieces.")
            
            # Llamar a la función de publicación
            success, result = publish_to_binance_square(content)
            
            if success:
                # Enviar confirmación a Telegram con el link del post
                share_link = ""
                if isinstance(result, dict):
                    share_link = result.get('data', {}).get('shareLink', '')
                confirm_msg = f"✅ *Publicado en Binance Square*\n🔗 [Ver post]({share_link})" if share_link else "✅ *Publicado exitosamente en Binance Square*"
                send_telegram_alert(confirm_msg)
                return web.json_response({'status': 'success', 'data': result})
            else:
                # Detectar si la API Key expiró y avisar
                if '220004' in str(result):
                    send_telegram_alert("🔑 *Tu API Key de Binance Square expiró.* Genera una nueva en Binance → Square → OpenAPI Settings y actualízala en Render.")
                return web.json_response({'status': 'error', 'message': result}, status=500)
                
        except Exception as e:
            logger.error(f"Error procesando el webhook de publicación: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)

    web_app = web.Application()
    web_app.router.add_get('/', handle_ping)
    web_app.router.add_post('/webhook/publish', handle_publish_webhook)
    
    # Render asigna el puerto automáticamente en la variable de entorno 'PORT'
    port = int(os.environ.get('PORT', 8080))
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Servidor Web dummy iniciado en el puerto {port} (Para Render)")
    # --- FIN DEL SERVIDOR WEB ---

    # Iniciar el recolector de datos infinitamente
    # Esto corre de forma concurrente con el Bot de Telegram
    await data_collection_loop()
    
    if app:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        
    await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Deteniendo Astro-Bot...")


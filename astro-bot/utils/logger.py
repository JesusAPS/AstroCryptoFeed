import logging
import sys
from logging.handlers import RotatingFileHandler
import os

# Asegurar que directorio de logs exista (Compatible local/Render sin Docker volume)
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name="AstroBot"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler (Rotativo: 5MB, 3 backups)
    log_file = os.path.join(LOG_DIR, "astro_bot.log")
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

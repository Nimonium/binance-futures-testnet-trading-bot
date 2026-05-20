import logging
import os
import time
from functools import wraps
from logging.handlers import RotatingFileHandler
from bot.config import Config

def setup_logging():
    """Configures rotating file logging for the application."""
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    log_file = os.path.join(Config.LOG_DIR, "trading.log")
    
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Rotating File Handler
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=Config.LOG_FILE_MAX_BYTES, 
            backupCount=Config.LOG_BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Professional formatting
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s - %(module)s:%(funcName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logging()

def time_execution(func):
    """Decorator to measure and log the execution time of API calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Executing {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000
            logger.debug(f"Completed {func.__name__} in {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"Failed {func.__name__} after {duration:.2f}ms due to {type(e).__name__}")
            raise
    return wrapper

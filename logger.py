import logging
from config import LOG_FILE

# 配置日志记录格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

logger = logging.getLogger('crypto_trading_bot')

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_success(message):
    logger.info(f"SUCCESS: {message}")

def log_debug(message):
    logger.debug(message)



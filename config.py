# config.py

# OKX Testnet API settings
API_KEY = "0b9fdb57-f8bb-476c-bda6-e11179f88780"
API_SECRET = "7653FCF2B58D83E928825C4B43974BA6"
API_PASSPHRASE = "Wumeiqing..123"
OKX_TESTNET_API_URL = "https://www.okx.com"

# ChatGPT API settings
CHATGPT_API_URL = "https://www.askapi.chat/v1/engines/ChatGPT4o/completions"
CHATGPT_API_KEY = "sk-4T3FIDUhdC91aR2b117e92Ad6e5b406393AdD05d4b1f4232"

# Trading parameters
TRADE_SYMBOL = "BTC-USDT-SWAP"
BASE_TRADE_AMOUNT_USDT = 100  # 基础交易金额，单位USDT
MIN_TRADE_AMOUNT_USDT = 15  # 最小交易金额
MAX_TRADE_AMOUNT_USDT = 500  # 最大交易金额
MAX_DAILY_TRADES = 100  # 每日最大交易次数
SYMBOL_BATCH_SIZE = 50  # 每次处理的币种数量
TRADE_INTERVAL = '1h'  # 交易级别：30分钟或1小时级别

# Database settings
DB_NAME = 'trading_bot.db'

# Scheduler settings
SCHEDULE_INTERVAL = 5  # minutes
WEEKLY_UPDATE_INTERVAL = 7  # days

# Monitoring settings
PROMETHEUS_PORT = 8000

# Logging
LOG_FILE = 'trading_log.txt'  # 日志文件


# For debugging purposes
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"CHATGPT_API_URL: {CHATGPT_API_URL}")
print(f"CHATGPT_API_KEY: {CHATGPT_API_KEY}")

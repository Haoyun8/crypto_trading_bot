# trading.py

import ccxt
import asyncio
import websockets
import json
from config import API_KEY, API_SECRET, API_PASSPHRASE, BASE_TRADE_AMOUNT_USDT, MAX_DAILY_TRADES, TRADE_INTERVAL, CHATGPT_API_URL, CHATGPT_API_KEY, OKX_TESTNET_API_URL
from logger import log_info, log_error, log_success
from database import Database
from chatgpt import AsyncChatGPT

class TradingBot:
    def __init__(self):
        log_info(f"API_KEY: {API_KEY}")
        log_info(f"API_SECRET: {API_SECRET}")
        log_info(f"API_PASSPHRASE: {API_PASSPHRASE}")
        log_info(f"CHATGPT_API_URL: {CHATGPT_API_URL}")
        log_info(f"CHATGPT_API_KEY: {CHATGPT_API_KEY}")

        self.exchange = ccxt.okx({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'password': API_PASSPHRASE,
            'enableRateLimit': True,
            'urls': {
                'api': OKX_TESTNET_API_URL
            }
        })
        self.db = Database()
        self.chatgpt = AsyncChatGPT()
        self.symbols = []

    async def place_order(self, symbol, side, amount_usdt, leverage):
        try:
            amount = amount_usdt / self.get_current_price(symbol)
            self.set_leverage(symbol, leverage)
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=amount
            )
            log_success(f"Order placed: {order}")
            self.db.insert_trade(symbol, amount, order['price'], side, "ChatGPT Strategy")
            self.print_balance_and_profit_loss()
        except Exception as e:
            log_error(f"Failed to place order: {e}")

    def set_leverage(self, symbol, leverage):
        self.exchange.privatePostAccountSetLeverage({
            'instId': symbol,
            'lever': leverage
        })

    def get_current_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def print_balance_and_profit_loss(self):
        try:
            balance = self.exchange.fetch_balance()
            log_info(f"Account balance: {balance['total']['USDT']}")
            positions = balance['info']['positions']
            for position in positions:
                if float(position['pos']) != 0:
                    symbol = position['instId']
                    unrealized_profit = position['upl']
                    log_info(f"Symbol: {symbol}, Unrealized Profit: {unrealized_profit}")
        except Exception as e:
            log_error(f"Error fetching balance and profit/loss: {e}")

    async def handle_market_data(self, symbol):
        log_info(f"Connecting to WebSocket for {symbol}...")
        try:
            async with websockets.connect(f'wss://ws.okx.com:8443/ws/v5/public?brokerId={symbol.lower().replace("/", "")}@kline_{TRADE_INTERVAL}') as websocket:
                log_info(f"Connected to WebSocket for {symbol}")
                while True:
                    data = await websocket.recv()
                    kline = json.loads(data)['data'][0]
                    market_data = {
                        "symbol": symbol,
                        "interval": TRADE_INTERVAL,
                        "open": kline['o'],
                        "close": kline['c'],
                        "high": kline['h'],
                        "low": kline['l'],
                        "volume": kline['vol'],
                        "timestamp": kline['ts']
                    }
                    log_info(f"Received market data for {symbol}: {market_data}")
                    await self.analyze_market_data(market_data)
        except Exception as e:
            log_error(f"Error handling market data for {symbol}: {e}")

    async def analyze_market_data(self, market_data):
        log_info(f"Analyzing market data for {market_data['symbol']}...")
        strategy = await self.chatgpt.get_strategy(market_data)
        if strategy:
            log_info(f"Received strategy for {market_data['symbol']}: {strategy}")
            daily_trade_count = self.db.fetch_daily_trade_count()
            if daily_trade_count >= MAX_DAILY_TRADES:
                log_info("Reached maximum daily trade limit, skipping trade.")
                return
            action = strategy['choices'][0]['message']['content']
            leverage = strategy['choices'][0]['message'].get('leverage', 1)  # Default leverage is 1
            if action == 'buy':
                await self.place_order(market_data['symbol'], 'buy', BASE_TRADE_AMOUNT_USDT, leverage)
            elif action == 'sell':
                await self.place_order(market_data['symbol'], 'sell', BASE_TRADE_AMOUNT_USDT, leverage)
        else:
            log_error(f"Failed to retrieve strategy for {market_data['symbol']} from ChatGPT.")

    async def get_top_symbols(self):
        try:
            tickers = self.exchange.fetch_tickers()
            # Convert tickers to the format ChatGPT expects
            market_data = [{"symbol": symbol, "quoteVolume": ticker['quoteVolume']} for symbol, ticker in tickers.items()]
            response = await self.chatgpt.get_top_symbols(market_data)
            if response:
                top_symbols = response['choices'][0]['message']['content']
                return top_symbols.split()  # Assuming the response is a space-separated string of symbols
            else:
                log_error("Failed to retrieve top symbols from ChatGPT.")
                return []
        except Exception as e:
            log_error(f"Error fetching top symbols: {e}")
            return []

    async def log_status(self):
        while True:
            log_info("Bot is running and analyzing market data...")
            for symbol in self.symbols:
                log_info(f"Currently monitoring: {symbol}")
            await asyncio.sleep(600)  # Log every 10 minutes

async def update_symbols():
    trading_bot = TradingBot()
    symbols = await trading_bot.get_top_symbols()
    db = Database()
    db.insert_symbols(symbols)
    log_info(f"Inserted top {len(symbols)} symbols into the database.")

async def main():
    await update_symbols()
    trading_bot = TradingBot()
    trading_bot.symbols = trading_bot.db.fetch_symbols()
    if not trading_bot.symbols:
        log_error("No symbols found in the database. Please ensure the symbols table is populated.")
        return
    trading_bot.print_balance_and_profit_loss()  # Print account balance at startup
    tasks = [trading_bot.handle_market_data(symbol) for symbol in trading_bot.symbols]
    tasks.append(trading_bot.log_status())  # Add status logging task
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())











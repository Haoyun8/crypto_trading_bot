import aiohttp
import asyncio
from config import CHATGPT_API_URL, CHATGPT_API_KEY
from logger import log_error

class AsyncChatGPT:
    def __init__(self):
        self.api_url = CHATGPT_API_URL
        self.api_key = CHATGPT_API_KEY

    async def get_strategy(self, market_data):
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a trading strategy generator."},
                {"role": "user", "content": f"Analyze the market data: {market_data}"}
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        for attempt in range(3):  # Retry mechanism
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.api_url, headers=headers, json=payload) as response:
                        response.raise_for_status()
                        return await response.json()
            except Exception as e:
                log_error(f"Error fetching strategy from ChatGPT (attempt {attempt+1}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        return None

    async def get_top_symbols(self, market_data):
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a market analyst."},
                {"role": "user", "content": f"Select the top 100 symbols based on trading opportunities: {market_data}"}
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        for attempt in range(3):  # Retry mechanism
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.api_url, headers=headers, json=payload) as response:
                        response.raise_for_status()
                        return await response.json()
            except Exception as e:
                log_error(f"Error fetching top symbols from ChatGPT (attempt {attempt+1}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        return None



from chatgpt import AsyncChatGPT

class SentimentAnalysis:
    def __init__(self):
        self.chatgpt = AsyncChatGPT()

    async def analyze_sentiment(self, text):
        response = await self.chatgpt.analyze_sentiment(f"Analyze sentiment for this text: {text}")
        return response

# Usage example
# async def main():
#     sa = SentimentAnalysis()
#     sentiment = await sa.analyze_sentiment("Bitcoin is rising fast")
#     print(sentiment)

# asyncio.run(main())

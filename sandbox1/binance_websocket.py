import asyncio
import websockets


async def hello():
    symbol = 'btcusdt'
    interval = '5m'
    uri = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(message)


asyncio.get_event_loop().run_until_complete(hello())

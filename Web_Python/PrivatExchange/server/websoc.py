import aiohttp
import asyncio
import logging

import websockets
from websockets import WebSocketServerProtocol, WebSocketProtocolError

from faker import Faker

logging.basicConfig(level=logging.INFO)


async def get_exchange():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as resp:
            if resp.status == 200:
                r = await resp.json()
                exc, = list(filter(lambda el: el['ccy'] == 'USD', r))
            return f"USD: buy: {exc['buy']}, sale: {exc['sale']}"


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.f_name = Faker().name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except WebSocketProtocolError as err:
            logging.error(err)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message == 'exchange':
                message = await get_exchange()
                await self.send_to_clients(message)
            else:
                await self.send_to_clients(f"{ws.f_name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 3000):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())

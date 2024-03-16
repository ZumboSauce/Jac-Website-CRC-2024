import asyncio
import random
import os


class BingoClientProtocol(asyncio.Protocol):
    clients: set[asyncio.Transport] = set()

    def connection_made(self, transport):
        print('Connection')
        BingoClientProtocol.clients.add(transport)
        self.transport = transport

    def connection_lost(self, exc):
        print('kys')
        BingoClientProtocol.clients.remove(self.transport)

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

class BingoGame():
    def __init__(self, call_interval: float):
        self.call_interval = call_interval
        self.game = asyncio.create_task(self.__bingo_roll(100, 4))

    async def __bingo_roll(self, rolls: int, timeout: float):
        for call in random.sample(range(rolls), rolls):
            next_call = asyncio.create_task(asyncio.sleep(timeout))
            for client in BingoClientProtocol.clients:
                client.write(f'\"call\": \"{call}\"'.encode())
            await next_call


async def main():
    loop = asyncio.get_running_loop()
    bingo = BingoGame(4)
    srv = await loop.create_unix_server(lambda: BingoClientProtocol(), "./assets/php/bingo.sock")
    os.chmod("./assets/php/bingo.sock", 0o777)
    async with srv:
        await srv.serve_forever()



if __name__ == "__main__":
    try:
        os.unlink("./assets/php/bingo.sock")
    except OSError:
        if os.path.exists("./assets/php/bingo.sock"):
            raise
    asyncio.run(main(), debug=True)
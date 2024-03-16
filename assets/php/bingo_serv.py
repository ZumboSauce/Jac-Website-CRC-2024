import asyncio

async def create_bingo_server(call_interval: int):
    srv = BingoServer(call_interval)
    await srv._init()
    return srv

class BingoServer:
    def __init__(self, call_interval: float):
        self.call_interval = call_interval

    async def _init(self):
        self.__gen = self.__bingo_roll_gen(100, self.call_interval)
        return None

    async def __bingo_roll_gen(self, rolls: int, interv: float):
        for call in random.sample(range(rolls), rolls):
            yield call
            await asyncio.sleep(interv)
    
    async def bingo_sse_handler(self, reader, writer: asyncio.StreamWriter):
        print("client")
        for call in self.__gen:
            writer.write(call)
            await writer.drain()


async def main():
    loop = asyncio.get_running_loop()
    bingo = await create_bingo_server(4)
    srv = await loop.create_unix_server(bingo.bingo_sse_handler, "./assets/php/bingo.sock")
    async with srv:
        await asyncio.Future()



if __name__ == "__main__":
    asyncio.run(main())
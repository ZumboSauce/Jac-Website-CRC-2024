from __future__ import annotations
import asyncio
import random
import os
import json
from mysql.connector.aio import connect, MySQLConnection
from collections import deque


_BINGO_QUEUE_SIZE:int = 7
_BINGO_CALL_INTERVAL:float = 4.0
_BINGO_MAX_NUM:int = 100


class BingoServer():
    def __init__(self):
        pass

    async def start_serving(self):
        self.bingo_roll = asyncio.create_task(self.__bingo_roll())
        conn = await connect(user="cheese", password="sudo", database="bingo")
        self.__handler.prep(conn)

    async def __bingo_roll(self):
        for call in random.sample(range(_BINGO_MAX_NUM), _BINGO_MAX_NUM):
            next_call = asyncio.create_task(asyncio.sleep(_BINGO_CALL_INTERVAL))
            self.__handler()._call_log.appendleft(call)
            for client in self.__handler()._client_pool:
                client.json_send('call', f'{[call]}')
            await next_call
    
    class __handler(asyncio.Protocol):
        __mysql_conn: MySQLConnection
        _client_pool: set[BingoServer.__handler] = set()
        _call_log: deque = deque(maxlen=_BINGO_QUEUE_SIZE)

        def __hash__(self):
            return hash(self.user_id)

        def __eq__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.user_id == other.user_id
        
        class __evt_handler():
            _evt_handlers = dict() 
            def __init__(self, f):
                self._evt_handlers.setdefault(f.__name__, f)
            def __call__(self):
                pass
        
        @classmethod
        def prep(cls, conn):
            cls.__mysql_conn = conn

        @__evt_handler
        async def bingo_subscribe(self, opt: dict):
            self._cleanup.add(self.__evt_handler._evt_handlers["bingo_unsubscribe"])
            self.user_id = opt['id']
            self._client_pool.add(self)
            if(opt['reconnect'] == "true"):
                self.json_send('call', [*self._call_log])

        @__evt_handler
        async def bingo_unsubscribe(self):
            self._client_pool.remove(self)
        
        @__evt_handler
        async def validate_spot(self, id: dict):
            cursor = await self.__mysql_conn.cursor()
            await cursor.execute(f"""UPDATE space
                                    INNER JOIN card ON space.card_id = card.id
                                    INNER JOIN user ON card.user_id = user.id
                                    SET called = 1
                                    WHERE number = {id['space_id']} AND space.card_id = {id['card_id']} AND card.user_id = {id['user_id']};""")
            self.json_send('resp', 1 if cursor.rowcount else 0)
            
        @__evt_handler
        async def request_card(self, id: int):
            cursor = await self.__mysql_conn.cursor()
            #check if thing existsrand
            c = []
            for i in range(0, 100, 10):
                j = random.sample(range(0, 10), 5)
                a = range(i, i+10)
                random.shuffle(a)
                it = iter(a)
                [[next(it) for __ in range(size)] for size in j]
                

                    

            
            pass

        def json_send(self, evt: str, data: str | int):
            self.transport.write(f'{{"{evt}": {data}}}'.encode())

        def connection_made(self, transport):
            self.transport = transport
            self._cleanup: set[callable] = set()

        def connection_lost(self, exc):
            for func in self._cleanup:
                task = asyncio.create_task(func(self))

        def data_received(self, msg):
            try:
                for evt, data in json.loads(msg).items():
                    task = asyncio.create_task(self.__evt_handler._evt_handlers[evt](self, data))

            except:
                print("malformed")
        #add del method to await and shit

    @classmethod
    def handler(cls):
        return cls.__handler

    

async def main():
    loop = asyncio.get_running_loop()
    bingo = BingoServer()
    await bingo.start_serving()
    srv = await loop.create_unix_server(bingo.handler(), "./assets/php/bingo.sock")
    os.chmod("./assets/php/bingo.sock", 0o777)
    async with srv:
        await srv.serve_forever()
    os.unlink("./assets/php/bingo.sock")



if __name__ == "__main__":
    try:
        os.unlink("./assets/php/bingo.sock")
    except OSError:
        if os.path.exists("./assets/php/bingo.sock"):
            raise
    asyncio.run(main(), debug=True)
from __future__ import annotations
import asyncio
import random
import os
import json
import aiomysql
from collections import deque
import pathlib
import numpy as np
import math

_BINGO_QUEUE_SIZE:int = 7
_BINGO_CALL_INTERVAL:float = 4.0
_BINGO_MAX_NUM:int = 100
_SOCK_PATH = pathlib.Path(__file__).parent.resolve() / 'bingo.sock'

class BingoServer():
    def __init__(self):
        pass

    async def start_serving(self):
        self.bingo_roll = asyncio.create_task(self.__bingo_roll())
        self.__handler.prep(await aiomysql.create_pool(host="localhost", port=3306, user="cheese", password="sudo", db="bingo"))

    async def __bingo_roll(self):
        for call in random.sample(range(_BINGO_MAX_NUM), _BINGO_MAX_NUM):
            next_call = asyncio.create_task(asyncio.sleep(_BINGO_CALL_INTERVAL))
            self.__handler()._call_log.appendleft(call)
            for client in self.__handler()._client_pool:
                client.json_send('call', f'{[call]}')
            await next_call
    
    class __handler(asyncio.Protocol):
        _db_pool: aiomysql.Pool
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
        def prep(cls, pool):
            cls._db_pool = pool

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
            async with self.__db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"""UPDATE space
                                            INNER JOIN card ON space.card_id = card.id
                                            INNER JOIN user ON card.user_id = user.id
                                            SET called = 1
                                            WHERE number = {id['space_id']} AND space.card_id = {id['card_id']} AND card.user_id = {id['user_id']};""")
                    self.json_send('resp', 1 if cur.rowcount() else 0)
            
        @__evt_handler
        async def request_cards(self, id: dict):
            async with self._db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(  f"""SELECT card.user_id, user.id
                                            from card
                                            INNER JOIN user ON card.user_id = user.id
                                            WHERE user.id = {id['user_id']}""")
                    if(cur.rowcount > 0):
                        cards = await cur.fetchall()
                        for card in cards:
                            await cur.execute( f"""SELECT space.card_id, card.id, card.user_id, user.id
                                                    from space
                                                    INNER JOIN card ON space.card_id = card.id
                                                    from card
                                                    INNER JOIN user ON card.user_id = user.id
                                                    WHERE space.card_id = {card['id']}""" )
                            spaces = await cur.fetchall()
                            for space in spaces:
                                print(space)
                    else:
                        cards = []
                        thing = [random.sample([idx for idx in range(col * 10, col * 10 + 10)], 10) for col in range(10)]
                        gen_rows = random.sample([[row for row in [thing[idx].pop() for idx in np.random.choice(range(10), size=5, replace=False, p=[len(col)/np.sum([len(col) for col in thing]) for col in thing])]] for _ in range(18)], 18)
                        for i in range(6):
                            card = dict()
                            rows = sorted(idx for row in [gen_rows.pop() for row in range(3)] for idx in row)
                            cols = [[items for items in rows if j*10 <= items < (j+1)*10] for j in range(9)]
                            for col in cols:
                                for idx, k in enumerate(sorted(random.sample(range(3), len(col)))):
                                    val = rows.pop(0)
                                    card[k * 10 + math.floor(val/10)] = val
                            await cur.execute( f"""INSERT INTO card (user_id)
                                                    VALUES ({id['user_id']})""")
                            card_id = cur.lastrowid
                            for key, item in card.items():                                    
                                await cur.execute ( f"""INSERT INTO space (idx, number, card_id)
                                                        VALUES ({key}, {item}, {card_id})""")
                        await cur.execute(  f"""SELECT card.user_id, user.id
                                                from card
                                                INNER JOIN user ON card.user_id = user.id
                                                WHERE user.id = {id['user_id']}""")
                        a = await cur.fetchall()
                        self.json_send('resp', a)
                        

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
                    print(evt)
                    print(data)
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
    srv = await loop.create_unix_server(bingo.handler(), _SOCK_PATH)
    _SOCK_PATH.chmod(0o777)
    async with srv:
        await srv.serve_forever()
    os.unlink(_SOCK_PATH)



if __name__ == "__main__":
    print(_SOCK_PATH)
    try:
        pathlib.Path.unlink(_SOCK_PATH)
    except OSError:
        pass
    asyncio.run(main(), debug=True)
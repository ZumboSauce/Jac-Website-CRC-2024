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
from aiohttp import web

_BINGO_QUEUE_SIZE:int = 7
_BINGO_CALL_INTERVAL:float = 4.0
_BINGO_MAX_NUM:int = 100
_SOCK_PATH = pathlib.Path(__file__).parent.resolve() / 'bingo.sock'

class BingoServer():
    def __init__(self):
        pass

    async def start_serving(self):
        srv = web.Application()
        srv.add_routes([web.get('/', self.__handler)])
        self.bingo_roll = asyncio.create_task(self.__bingo_roll())
        self.__handler.prep(await aiomysql.create_pool(host="localhost", port=3306, user="cheese", password="sudo", db="bingo"))
        web.run_app(srv)

    async def __bingo_roll(self):
        #deal with sending taking more time than timeout ?
        for call in random.sample(range(_BINGO_MAX_NUM), _BINGO_MAX_NUM):
            next_call = asyncio.create_task(asyncio.sleep(_BINGO_CALL_INTERVAL))
            self.__handler()._call_log.appendleft(call)
            for client in self.__handler()._client_pool:
                self.__handler.sse_event(client, "call", {"call": call})
            await next_call
    
    class __handler(asyncio.Protocol):
        _client_pool: set[BingoServer.__handler] = set()
        async def __call__(self, request: web.Request):
            resp = web.StreamResponse(headers={'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache'})
            resp.prepare()
            self._client_pool.add(resp)
            await asyncio.Future()
            self._client_pool.remove(resp)
            return resp
        
        @staticmethod
        async def sse_event(stream: web.StreamResponse, evt: str, data: dict):
            await stream.write(f"event: {evt}\ndata: {json.dumps(data)}\n\n")

    class __api():
        _db_pool: aiomysql.Pool
        _call_log: deque = deque(maxlen=_BINGO_QUEUE_SIZE)
        
        class __evt_handler():
            _evt_handlers = dict() 
            def __init__(self, f):
                self._evt_handlers.setdefault(f.__name__, f)
            def __call__(self):
                pass

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
        def prep(cls, pool):
            cls._db_pool = pool
        
        @__evt_handler
        async def check_spot(self, arg: dict):
            async with self.__db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(   """UPDATE space
                                            INNER JOIN card ON space.card_id = card.id
                                            INNER JOIN user ON card.user_id = user.id
                                            SET called = 1
                                            WHERE number = %d AND space.id = %d AND space.card_id = %d AND card.user_id = %d ;""", (arg['space_number'], arg['space_id'], arg['card_id'], arg['user_id'], )
                                        )
                    self.json_send('resp', 1 if cur.rowcount() else 0)
            
        @__evt_handler
        async def request_cards(self, arg: dict):
            async with self._db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(  """SELECT card.user_id, user.id
                                            from card
                                            INNER JOIN user ON card.user_id = user.id
                                            WHERE user.id = %d""", ({arg['user_id']},))
                    if(cur.rowcount > 0):
                        cards = await cur.fetchall()
                        for card in cards:
                            await cur.execute( """SELECT space.card_id, card.id, card.user_id, user.id
                                                    from space
                                                    INNER JOIN card ON space.card_id = card.id
                                                    from card
                                                    INNER JOIN user ON card.user_id = user.id
                                                    WHERE space.card_id = %d""", ({card['id']},))
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
                            cols = [[items for items in rows if j*10 <= items < (j+1)*10] for j in range(10)]
                            for col in cols:
                                for idx, k in enumerate(sorted(random.sample(range(3), len(col)))):
                                    val = rows.pop(0)
                                    card[k * 10 + math.floor(val/10)] = val
                            await cur.execute( """INSERT INTO card (user_id)
                                                    VALUES (%d)""", ({id['user_id']},))
                            card_id = cur.lastrowid
                            #use the execute many thing
                            for key, item in card.items():                                    
                                await cur.execute ( f"""INSERT INTO space (idx, number, card_id)
                                                        VALUES ({key}, {item}, {card_id})""")
                        await cur.execute(  f"""SELECT card.user_id, user.id
                                                from card
                                                INNER JOIN user ON card.user_id = user.id
                                                WHERE user.id = {id['user_id']}""")
                        a = await cur.fetchall()
                        self.json_send('resp', a)


    

async def main():
    app = web.Application()

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
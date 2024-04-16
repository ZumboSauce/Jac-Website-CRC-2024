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
import itertools

_BINGO_QUEUE_SIZE:int = 7
_BINGO_CALL_INTERVAL:float = 4.0
_BINGO_MAX_NUM:int = 100
_SOCK_PATH = pathlib.Path(__file__).parent.resolve() / 'bingo.sock'

class BingoServer():
    def __init__(self):
        pass

    async def start_serving(self):
        self.bingo_roll = asyncio.create_task(self.__bingo_roll())
        self.db_pool = await aiomysql.create_pool(host="localhost", port=3306, user="cheese", password="sudo", db="bingo", autocommit=True)
        
        #await self.game_prep()

        srv = web.Application()
        srv.add_routes([web.get('/', self.__sse_handler())])
        runner = web.AppRunner(srv, handler_cancellation=True)
        await runner.setup()
        sse_site = web.TCPSite(runner)
        await sse_site.start()

        pathlib.Path.unlink(_SOCK_PATH, True)
        self.api = self.__api()
        await self.api.prep(self.db_pool)
        api = await asyncio.start_unix_server(self.api._handler, _SOCK_PATH)
        await api.start_serving()
        _SOCK_PATH.chmod(0o777)
        print("done")

    async def __bingo_roll(self):
        #deal with sending taking more time than timeout ?
        for call in random.sample(range(_BINGO_MAX_NUM), _BINGO_MAX_NUM):
            next_call = asyncio.create_task(asyncio.sleep(_BINGO_CALL_INTERVAL))
            self.__sse_handler._call_log.appendleft(call)
            self.__api._call_log.appendleft(call)
            for client in self.__sse_handler._client_pool:
                await self.__sse_handler.sse_event(client, "call", {"call": call})
            await next_call

    class __sse_handler():
        _call_log: deque = deque(maxlen=_BINGO_QUEUE_SIZE)
        _client_pool: set[BingoServer.__sse_handler] = set()

        def __init__(self):
            pass

        async def __call__(self, request: web.Request):
            resp = web.StreamResponse(headers={'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache'})
            await resp.prepare(request)
            self._client_pool.add(resp)
            print("cum")
            try:
                await asyncio.Future()
            except:
                print("dick")
                self._client_pool.remove(resp)
                return resp
        
        @staticmethod
        async def sse_event(stream: web.StreamResponse, evt: str, data: dict):
            await stream.write(f"event: {evt}\ndata: {json.dumps(data)}\n\n".encode())

    class __api():
        _call_log: deque = deque(maxlen=_BINGO_QUEUE_SIZE)
        def __init__(self):
            pass

        class __evt_handler():
            _evt_handlers = dict() 
            def __init__(self, f):
                self._evt_handlers.setdefault(f.__name__, f)

        async def _handler(self, r: asyncio.StreamReader, w: asyncio.StreamWriter):
            query = (await r.read(200)).decode()
            print(query)
            for evt, data in json.loads(query).items():
                task = asyncio.create_task(self.__evt_handler._evt_handlers[evt](self, data))
                w.write(json.dumps(await task).encode())
            w.write_eof()

        async def prep(self, pool: aiomysql.Pool):
            self._db_pool = pool
            async with self._db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(  """TRUNCATE TABLE space;
                                            TRUNCATE TABLE card;""")
        
        @__evt_handler
        async def check_spot(self, arg: dict):
            if(arg['space_number'] not in self._call_log): return {'resp': 0}
            async with self._db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(   """UPDATE space
                                            INNER JOIN card ON space.card_id = card.id
                                            INNER JOIN user ON card.user_id = user.id
                                            SET called = 1
                                            WHERE number = %s AND card.user_id = %s ;""", (arg['space_number'], arg['user_id'], )
                                        )
                    print(cur.rowcount)
                    return {'resp': 1 if cur.rowcount else 0}
            
        @__evt_handler
        async def request_cards(self, arg: dict):
            async with self._db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(  """SELECT card.id
                                            from card
                                            INNER JOIN user 
                                            ON card.user_id = user.id
                                            WHERE user.id = %s""", (arg['user_id'],))
                    if(cur.rowcount > 0):
                        cards = []
                        card_ids = await cur.fetchall()
                        for card_id in card_ids:
                            await cur.execute( """SELECT idx, number, called
                                                    from space as s
                                                    INNER JOIN 
                                                    card as c
                                                    ON s.card_id = c.id
                                                    INNER JOIN
                                                    user as u
                                                    ON c.user_id = u.id
                                                    WHERE s.card_id = %s""", (card_id['id'],))
                            cards.append(await cur.fetchall())
                        return {"resp": cards}
                    else:
                        cards = []
                        gen_rows = []
                        while True:
                            try:
                                thing = [random.sample([idx for idx in range(col * 10, col * 10 + 10)], 10) for col in range(9)]
                                gen_rows = random.sample([[row for row in [thing[idx].pop() for idx in np.random.choice(range(9), size=5, replace=False, p=[len(col)/np.sum([len(col) for col in thing]) for col in thing])]] for _ in range(18)], 18)
                            except:
                                continue
                            break
                        p = lambda d: zip(d.keys(), sorted(d.values()))
                        for i in range(6):
                            card_sorted = dict()
                            a = [sorted(gen_rows.pop())+[0] for _ in range(3)]
                            for j in range(9):
                                card_sorted.update( {k*9+j:v for k,v in p( { idx:row.pop(0) for idx, row in enumerate(a) if j*10 <= row[0] < (j+1)*10 } ) } )
                                                
                            await cur.execute( """INSERT INTO card (spaces_left, user_id)
                                                    VALUES (%s, %s)""", (15, arg['user_id'],))
                            card_id = cur.lastrowid
                            for key, item in card_sorted.items():                                    
                                await cur.execute ( """INSERT INTO space (idx, number, card_id)
                                                        VALUES (%s, %s, %s)""", (key, item, card_id,))
                            await cur.execute(  """SELECT idx, number, called
                                                        FROM space
                                                        WHERE card_id = (%s)""", card_id)
                            cards.append(await cur.fetchall())
                        return {'resp': cards}

    

async def main():
    bingo = BingoServer()
    await bingo.start_serving()
    await asyncio.Future()
    os.unlink(_SOCK_PATH)



if __name__ == "__main__":
    print(_SOCK_PATH)
    try:
        pathlib.Path.unlink(_SOCK_PATH)
    except OSError:
        pass
    asyncio.run(main(), debug=True)
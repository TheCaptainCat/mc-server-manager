import asyncio
from typing import List

import websockets

from server_rnr import MCRunner


class WSConnection:
    def __init__(self, runner: MCRunner):
        self.runner = runner
        self._out_queue = asyncio.Queue()
        self._in_queue = asyncio.Queue()

    async def push_message(self, message: str):
        await self._out_queue.put(message)

    async def _wait_for_messages(self):
        while True:
            args: List[str] = (await self._in_queue.get()).split(':')
            if len(args) <= 0:
                continue
            action = args[0].lower()
            args = args[1:]
            if action == 'status':
                await self.push_message(f'STATUS:{self.runner.status}')
            elif action == 'update' and len(args) == 1:
                self.runner.update(':'.join(args))
            elif action == 'run':
                self.runner.run()
            elif action == 'command':
                self.runner.write(':'.join(args))

    def _consumer(self):
        async def consumer_handler(websocket, _):
            try:
                async for message in websocket:
                    await self._in_queue.put(message)
            except websockets.exceptions.ConnectionClosedError:
                return
        return consumer_handler

    def _producer(self):
        async def producer_handler(websocket, _):
            while True:
                message = await self._out_queue.get()
                await websocket.send(message)
        return producer_handler

    @staticmethod
    def ws_handler(runner: MCRunner):
        async def handler(websocket, path):
            ws = WSConnection(runner)
            runner.register_connection(ws)
            msg_task = asyncio.create_task(ws._wait_for_messages())
            consumer_task = asyncio.create_task(ws._consumer()(websocket, path))
            producer_task = asyncio.create_task(ws._producer()(websocket, path))
            try:
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task, msg_task],
                    return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()
                for task in done:
                    task.result()
            finally:
                runner.unregister_connection(ws)
        return handler

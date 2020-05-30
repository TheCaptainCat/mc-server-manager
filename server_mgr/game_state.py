import asyncio
import websockets

from bolinette import core


class GameState:
    def __init__(self, context: core.BolinetteContext):
        self._status = None
        self.context = context
        self._in_queue = asyncio.Queue()
        self._out_queue = asyncio.Queue()

    @property
    def status(self):
        return self._status

    async def _process_message(self, message: str):
        action, args = message.split(':', 1)
        if action == 'STATUS':
            self._status = args
            await self.context.sockets.send_message('game', 'status', {
                'status': args
            })
        elif action == 'INSTALLED':
            version = await self.context.service('version').get_by_name(args)
            await self.context.service('version').set_installed(version)
            await self.context.sockets.send_message('game', 'version', {
                'installed': version.name
            })
        elif action == 'UPDATING':
            done, total = args.split(':')
            await self.context.sockets.send_message('game', 'update', {
                'done': int(done),
                'total': int(total)
            })
        elif action == 'LOG':
            await self.context.sockets.send_message('game', 'log', {
                'content': args
            })

    def _consumer(self):
        async def consumer_handler(websocket: websockets.WebSocketClientProtocol):
            while True:
                await self._process_message(await websocket.recv())
        return consumer_handler

    def _producer(self):
        async def producer_handler(websocket: websockets.WebSocketClientProtocol):
            while True:
                message: str = await self._out_queue.get()
                await websocket.send(message)
        return producer_handler

    async def push_message(self, message):
        await self._out_queue.put(message)

    async def query_status(self):
        await self.push_message('STATUS')

    async def run_game(self):
        await self.push_message('RUN')

    async def stop_game(self):
        await self.push_message('COMMAND:stop')

    async def open_connection(self):
        async with websockets.connect('ws://localhost:4242/') as websocket:
            consumer_task = asyncio.create_task(self._consumer()(websocket))
            producer_task = asyncio.create_task(self._producer()(websocket))
            try:
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()
                for task in done:
                    task.result()
            finally:
                pass

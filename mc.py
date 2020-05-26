import asyncio
import os

import websockets

from server_rnr import MCRunner

if __name__ == '__main__':
    runner = MCRunner(os.path.join(os.getcwd(), 'minecraft'))
    start_server = websockets.serve(runner.get_ws_handler(), '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

import asyncio

from bolinette import core
from bolinette.decorators import init_func

from server_mgr.game import GameState


@init_func
def init_ws_connection(context: core.BolinetteContext):
    async def _init(app):
        state = GameState(context)
        app['blnt']['mc'] = state
        asyncio.create_task(state.open_connection())
        await state.query_status()
    context.app.on_startup.append(_init)

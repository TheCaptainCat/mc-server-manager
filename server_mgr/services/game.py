from bolinette import blnt
from bolinette.decorators import service

from server_mgr import GameState
from server_mgr.services import PropertyService


@service('game')
class GameService(blnt.SimpleService):
    @property
    def game_state(self) -> GameState:
        return self.context['mc']

    @property
    def prop_service(self) -> PropertyService:
        return self.context.service('prop')

    async def send_command(self, command: str):
        rcon_password = await self.prop_service.get_by_name('rcon.password')
        rcon_port = await self.prop_service.get_by_name('rcon.port')
        if rcon_password and rcon_port:
            return await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value), command)

    async def get_game_status(self):
        return self.game_state.status

    async def run_game(self):
        await self.prop_service.commit_properties()
        await self.game_state.run_game()

    async def stop_game(self):
        await self.game_state.stop_game()

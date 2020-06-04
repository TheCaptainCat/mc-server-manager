from bolinette import blnt
from bolinette.decorators import get, post, controller
from bolinette.utils import response

from server_mgr.services import VersionService, GameService


@controller('game', '/game')
class GameController(blnt.Controller):
    @property
    def version_service(self) -> VersionService:
        return self.context.service('version')

    @property
    def game_service(self) -> GameService:
        return self.context.service('game')

    @get('/status')
    async def get_status(self, **_):
        latest = await self.version_service.get_latest()
        installed = await self.version_service.get_installed()
        return response.ok('OK', {
            'status': await self.game_service.get_game_status(),
            'installed': installed.name if installed else None,
            'latest': latest.name if latest else None
        })

    @get('/versions', returns=('version', 'short', 'as_list'))
    async def get_versions(self, **_):
        return response.ok('OK', await self.version_service.get_all(order_by=[('date', False)]))

    @post('/install/{version}', returns='version')
    async def install_version(self, match, **_):
        version = await self.version_service.get_by_name(match['version'])
        await self.version_service.download_server(version)
        return response.ok('OK', version)

    @post('/run')
    async def run_game(self, **_):
        await self.game_service.run_game()
        return response.ok('OK')

    @post('/stop')
    async def stop_game(self, **_):
        await self.game_service.stop_game()
        return response.ok('OK')

    @post('/command')
    async def run_command(self, payload, **_):
        result = await self.game_service.send_command(payload['command'])
        return response.ok('OK', {'result': result})

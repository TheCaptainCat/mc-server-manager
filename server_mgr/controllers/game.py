import asyncio

from bolinette import data
from bolinette.decorators import get, post, controller
from bolinette.utils import response


@controller('game', '/game')
class GameController(data.Controller):
    @property
    def setting_service(self):
        return self.context.service('setting')

    @property
    def version_service(self):
        return self.context.service('version')

    @get('/installed')
    async def get_versions(self, **_):
        installed = await self.setting_service.get_setting('installed_version')
        latest = await self.version_service.get_latest()
        return response.ok('OK', {
            'installed': installed.value if installed else None,
            'latest': latest.name if latest else None
        })

    @post('/install/{version}',
          returns='version')
    async def install_version(self, match, **_):
        version = await self.version_service.get_by_name(match['version'])
        # await self.version_service.download_server(version)
        asyncio.create_task(self.version_service.download_server(version))
        return response.ok('OK', version)

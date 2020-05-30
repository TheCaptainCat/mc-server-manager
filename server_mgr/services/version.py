import json
from datetime import datetime

import requests
from bolinette import blnt
from bolinette.decorators import service

from server_mgr import GameState


@service('version')
class VersionService(blnt.Service):
    @property
    def game_state(self) -> GameState:
        return self.context['mc']

    async def refresh_cache(self):
        cached = dict(map(lambda v: (v.name, v), await self.get_all()))
        fetched = json.loads(
            requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').content
        )['versions']
        for version in fetched:
            if version['id'] not in cached:
                await self.create({
                    'name': version['id'],
                    'v_type': version['type'],
                    'url': version['url'],
                    'date': datetime.fromisoformat(version['releaseTime']),
                    'installed': False
                })
        return await self.get_all()

    async def get_by_name(self, name):
        return await self.get_first_by('name', name)

    async def get_latest(self):
        await self.refresh_cache()
        version_table = self.context.table('version')
        return self.repo.query.order_by(blnt.functions.desc(version_table.date)).first()

    async def get_installed(self):
        return await self.get_first_by('installed', True, safe=True)

    async def set_installed(self, version):
        installed = await self.get_installed()
        if installed is not None:
            installed.installed = False
        version.installed = True

    async def download_server(self, version):
        await self.game_state.push_message(f'UPDATE:{version.name}')

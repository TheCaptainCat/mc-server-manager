import asyncio
import json
from datetime import datetime

import requests
from bolinette import data
from bolinette.decorators import service
from bolinette.utils import fs


@service('version')
class VersionService(data.Service):
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
                    'date': datetime.fromisoformat(version['releaseTime'])
                })
        return await self.get_all()

    async def get_by_name(self, name):
        return await self.get_first_by('name', name)

    async def get_latest(self):
        await self.refresh_cache()
        version_table = self.context.table('version')
        return self.repo.query.order_by(data.functions.desc(version_table.date)).first()

    async def download_server(self, version):
        pass

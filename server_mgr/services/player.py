import json

import requests
from bolinette import blnt
from bolinette.decorators import service
from bolinette.exceptions import NotFoundError


@service('player')
class PlayerService(blnt.Service):
    async def create(self, values, **_):
        values['balance'] = 0
        values['uid'] = self.fetch_uid(values['name'])
        return await super().create(values, **_)

    def fetch_uid(self, username):
        url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
        resp = requests.get(url).content
        if not resp:
            raise NotFoundError(f'game.player.not_found')
        return json.loads(resp)['id']

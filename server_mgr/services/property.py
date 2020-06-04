import random
import string
from typing import List, Dict

from bolinette import blnt, env
from bolinette.decorators import service


@service('prop')
class PropertyService(blnt.Service):
    async def accept_eula(self):
        with open(env.root_path('minecraft', 'eula.txt'), 'w+') as f:
            f.write('eula=true\n')

    async def commit_properties(self):
        await self.reset_rcon_password()
        with open(env.root_path('minecraft', 'server.properties'), 'w+') as f:
            for prop in await self.get_all():
                f.write(f'{prop.name}={prop.value}\n')

    async def get_by_name(self, name: str):
        return await self.get_first_by('name', name)

    async def get_unprotected(self):
        return self.repo.query.filter_by(**{'protected': False}).all()

    async def reset_rcon_password(self):
        prop = await self.get_by_name('rcon.password')
        if prop:
            prop.value = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    async def update_all(self, props: List[Dict[str, str]]):
        properties = []
        for p in props:
            if 'name' in p and 'value' in p:
                prop = await self.get_by_name(p['name'])
                if prop:
                    prop.value = p['value']
                    properties.append(prop)
        return properties

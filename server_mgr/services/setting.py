from bolinette import data
from bolinette.decorators import service


@service('setting')
class SettingService(data.Service):

    async def get_setting(self, name):
        return await self.get_first_by('name', name)

    async def set_setting(self, name, value):
        setting = await self.get_setting(name)
        await self.patch(setting, {'value': value})

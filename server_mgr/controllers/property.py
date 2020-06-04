from bolinette import blnt
from bolinette.decorators import controller, post, get, put
from bolinette.utils import response

from server_mgr.services import PropertyService


@controller('prop', '/prop')
class PropertyController(blnt.Controller):
    @property
    def prop_service(self) -> PropertyService:
        return self.context.service('prop')

    @post('/eula/accept', roles=['admin'])
    async def accept_eula(self, **_):
        await self.prop_service.accept_eula()
        return response.ok('OK')

    @get('', roles=['admin'], returns=('prop', 'default', 'as_list'))
    async def get_all(self, **_):
        return response.ok('OK', await self.prop_service.get_unprotected())

    @put('', roles=['admin'], returns=('prop', 'default', 'as_list'))
    async def save_all(self, payload, **_):
        return response.ok('OK', await self.prop_service.update_all(payload))

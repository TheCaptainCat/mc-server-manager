from bolinette import core
from bolinette.decorators import seeder
from bolinette.defaults.services import RoleService, UserService


@seeder
async def role_seeder(context: core.BolinetteContext):
    role_service: RoleService = context.service('role')
    with core.Transaction(context):
        await role_service.create({'name': 'root'})
        await role_service.create({'name': 'admin'})


@seeder
async def dev_user_seeder(context: core.BolinetteContext):
    role_service: RoleService = context.service('role')
    user_service: UserService = context.service('user')
    with core.Transaction(context):
        root_role = await role_service.get_by_name('root')
        root_user = await user_service.create({
            'username': 'root',
            'password': 'root',
            'email': 'root@localhost'
        })
        root_user.roles.append(root_role)

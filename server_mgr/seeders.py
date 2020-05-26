from bolinette import core, env
from bolinette.decorators import seeder
from bolinette.defaults.services import RoleService, UserService

from server_mgr.services import SettingService


@seeder
async def settings_seeder(context: core.BolinetteContext):
    setting_service: SettingService = context.service('setting')
    with core.Transaction(context):
        await setting_service.create({'name': 'installed_version', 'value': None})


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
    if env['PROFILE'] == 'development':
        with core.Transaction(context):
            root = await role_service.get_by_name('root')
            admin = await role_service.get_by_name('admin')
            root_usr = await user_service.create({
                'username': 'root',
                'password': 'root',
                'email': f'root@localhost'
            })
            root_usr.roles.append(root)
            root_usr.roles.append(admin)

            dev0 = await role_service.create({'name': 'dev0'})
            dev1 = await role_service.create({'name': 'dev1'})
            dev2 = await role_service.create({'name': 'dev2'})
            roles = [dev0, dev1, dev2]

            for i in range(10):
                user = await user_service.create({
                    'username': f'user_{i}',
                    'password': 'test',
                    'email': f'user{i}@test.com'
                })
                user.roles.append(roles[i % 3])
                user.roles.append(roles[(i + 1) % 3])

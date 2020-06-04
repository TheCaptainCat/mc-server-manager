from bolinette import core
from bolinette.decorators import seeder
from bolinette.defaults.services import RoleService, UserService

from server_mgr.services import PropertyService


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


@seeder
async def properties_seeder(context: core.BolinetteContext):
    prop_service: PropertyService = context.service('prop')
    with core.Transaction(context):
        properties = [
            {'name': 'enable-jmx-monitoring', 'value': 'false', 'protected': False},
            {'name': 'rcon.port', 'value': '25575', 'protected': True},
            {'name': 'level-seed', 'value': '', 'protected': False},
            {'name': 'gamemode', 'value': 'survival', 'protected': False},
            {'name': 'enable-command-block', 'value': 'false', 'protected': False},
            {'name': 'enable-query', 'value': 'false', 'protected': False},
            {'name': 'generator-settings', 'value': '', 'protected': False},
            {'name': 'level-name', 'value': 'world', 'protected': False},
            {'name': 'motd', 'value': 'A Minecraft Server', 'protected': False},
            {'name': 'query.port', 'value': '25565', 'protected': False},
            {'name': 'pvp', 'value': 'true', 'protected': False},
            {'name': 'generate-structures', 'value': 'true', 'protected': False},
            {'name': 'difficulty', 'value': 'easy', 'protected': False},
            {'name': 'network-compression-threshold', 'value': '256', 'protected': False},
            {'name': 'max-tick-time', 'value': '60000', 'protected': False},
            {'name': 'max-players', 'value': '20', 'protected': False},
            {'name': 'use-native-transport', 'value': 'true', 'protected': False},
            {'name': 'online-mode', 'value': 'true', 'protected': False},
            {'name': 'enable-status', 'value': 'true', 'protected': False},
            {'name': 'allow-flight', 'value': 'false', 'protected': False},
            {'name': 'broadcast-rcon-to-ops', 'value': 'true', 'protected': False},
            {'name': 'view-distance', 'value': '10', 'protected': False},
            {'name': 'max-build-height', 'value': '256', 'protected': False},
            {'name': 'server-ip', 'value': '', 'protected': False},
            {'name': 'allow-nether', 'value': 'true', 'protected': False},
            {'name': 'server-port', 'value': '25565', 'protected': False},
            {'name': 'enable-rcon', 'value': 'true', 'protected': True},
            {'name': 'sync-chunk-writes', 'value': 'true', 'protected': False},
            {'name': 'op-permission-level', 'value': '4', 'protected': False},
            {'name': 'prevent-proxy-connections', 'value': 'false', 'protected': False},
            {'name': 'resource-pack', 'value': '', 'protected': False},
            {'name': 'entity-broadcast-range-percentage', 'value': '100', 'protected': False},
            {'name': 'rcon.password', 'value': '', 'protected': True},
            {'name': 'player-idle-timeout', 'value': '0', 'protected': False},
            {'name': 'force-gamemode', 'value': 'false', 'protected': False},
            {'name': 'hardcore', 'value': 'false', 'protected': False},
            {'name': 'white-list', 'value': 'false', 'protected': False},
            {'name': 'broadcast-console-to-ops', 'value': 'true', 'protected': False},
            {'name': 'spawn-npcs', 'value': 'true', 'protected': False},
            {'name': 'spawn-animals', 'value': 'true', 'protected': False},
            {'name': 'snooper-enabled', 'value': 'true', 'protected': False},
            {'name': 'function-permission-level', 'value': '2', 'protected': False},
            {'name': 'level-type', 'value': 'default', 'protected': False},
            {'name': 'spawn-monsters', 'value': 'true', 'protected': False},
            {'name': 'enforce-whitelist', 'value': 'false', 'protected': False},
            {'name': 'resource-pack-sha1', 'value': '', 'protected': False},
            {'name': 'spawn-protection', 'value': '16', 'protected': False},
            {'name': 'max-world-size', 'value': '29999984', 'protected': False},
        ]
        for prop in properties:
            await prop_service.create(prop)

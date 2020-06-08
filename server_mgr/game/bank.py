import re

from bolinette import core

from server_mgr import game, services


class MCBank:
    def __init__(self, context: core.BolinetteContext):
        self.context = context
        self._rule = re.compile(r'^\[(?:\d\d:?){3}\] \[[^\]]*\]: <(?P<name>[^>]*)> !bank ?(?P<command>.*)$')
        self._xp_rule = re.compile(r'.* has (?P<xp>\d*) experience levels')

    @property
    def player_service(self) -> 'services.PlayerService':
        return self.context.service('player')

    @property
    def prop_service(self) -> 'services.PropertyService':
        return self.context.service('prop')

    @property
    def game_state(self) -> 'game.GameState':
        return self.context['mc']

    async def process(self, text):
        rcon_password = await self.prop_service.get_by_name('rcon.password')
        rcon_port = await self.prop_service.get_by_name('rcon.port')
        if rcon_password is None or rcon_port is None:
            return
        match = self._rule.match(text)
        if match is None:
            return
        name = match.group('name')
        command = match.group('command')
        player = await self.player_service.get_by_name(name, safe=True)
        if player is None:
            await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value),
                                                    f'msg {name} You are not registered in the bank! Ask a mod')
            return
        xp = int(self._xp_rule.match(
            await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value),
                                                    f'xp query {player.name} levels')).group('xp'))
        with core.Transaction(self.context):
            args = command.strip().split(' ')
            if len(args) >= 1:
                if args[0] == 'add' and len(args) == 2:
                    if args[1] == 'all':
                        amount = xp
                    else:
                        amount = min(xp, int(args[1]))
                    player.balance += amount
                    await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value),
                                                            f'xp set {player.name} {xp - amount} levels')
                elif args[0] == 'get' and len(args) == 2:
                    if args[1] == 'all':
                        amount = xp
                    else:
                        amount = min(player.balance, int(args[1]))
                    player.balance -= amount
                    await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value),
                                                            f'xp add {player.name} {amount} levels')
        await self.game_state.push_rcon_command(rcon_password.value, int(rcon_port.value),
                                                f'msg {name} You have now {player.balance} in bank')

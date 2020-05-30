from bolinette import blnt
from bolinette.decorators import controller


@controller('player', '/player')
class PlayerController(blnt.Controller):
    def default_routes(self):
        return [
            self.defaults.get_all(),
            self.defaults.create(roles=['admin'])
        ]

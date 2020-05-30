from bolinette import blnt
from bolinette.decorators import service


@service('game')
class GameService(blnt.SimpleService):
    pass

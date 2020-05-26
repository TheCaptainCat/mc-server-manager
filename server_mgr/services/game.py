from bolinette import data
from bolinette.decorators import service


@service('game')
class GameService(data.SimpleService):
    pass

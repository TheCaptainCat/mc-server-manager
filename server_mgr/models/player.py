from bolinette import blnt, types
from bolinette.decorators import model


@model('player')
class Player(blnt.Model):
    id = types.defs.Column(types.db.Integer, primary_key=True)
    name = types.defs.Column(types.db.String, nullable=False)
    uid = types.defs.Column(types.db.String, nullable=False)
    balance = types.defs.Column(types.db.Integer, nullable=False)

    @classmethod
    def payloads(cls):
        yield [
            types.mapping.Column(cls.name, required=True)
        ]

    @classmethod
    def responses(cls):
        yield [
            types.mapping.Column(cls.uid),
            types.mapping.Column(cls.name),
            types.mapping.Column(cls.balance)
        ]



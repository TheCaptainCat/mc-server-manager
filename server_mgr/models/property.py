from bolinette import blnt, types
from bolinette.decorators import model


@model('prop')
class Property(blnt.Model):
    id = types.defs.Column(types.db.Integer, primary_key=True)
    name = types.defs.Column(types.db.String, nullable=False)
    value = types.defs.Column(types.db.String, nullable=False)
    protected = types.defs.Column(types.db.Boolean, nullable=False)

    @classmethod
    def payloads(cls):
        yield []

    @classmethod
    def responses(cls):
        yield [
            types.mapping.Column(cls.name),
            types.mapping.Column(cls.value),
        ]

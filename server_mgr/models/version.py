from bolinette import data, types
from bolinette.decorators import model


@model('version')
class Version(data.Model):
    id = types.defs.Column(types.db.Integer, primary_key=True)
    name = types.defs.Column(types.db.String, nullable=False)
    v_type = types.defs.Column(types.db.String, nullable=False)
    date = types.defs.Column(types.db.Date, nullable=False)
    url = types.defs.Column(types.db.String, nullable=False)

    @classmethod
    def payloads(cls):
        yield []

    @classmethod
    def responses(cls):
        yield [
            types.mapping.Column(cls.name),
            types.mapping.Column(cls.v_type),
            types.mapping.Column(cls.date),
            types.mapping.Column(cls.url)
        ]

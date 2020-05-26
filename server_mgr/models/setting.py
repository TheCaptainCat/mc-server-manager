from bolinette import data, types
from bolinette.decorators import model


@model('setting')
class Setting(data.Model):
    id = types.defs.Column(types.db.Integer, primary_key=True)
    name = types.defs.Column(types.db.String, nullable=False)
    value = types.defs.Column(types.db.String)

import peewee as pw
from upact.models.base_model import BaseModel
from upact.models.uri import Uri

class PlaytimeRule(BaseModel):
    from_time = pw.TimeField()
    to_time = pw.TimeField()
    frequency = pw.CharField()
    uri = pw.ForeignKeyField(Uri, backref='playtime_rules')

import peewee as pw

from upact.models.base_model import BaseModel
from upact.models.uri import Uri

class BlockedIp(BaseModel):
    address = pw.CharField()
    uri = pw.ForeignKeyField(Uri, backref='ips')
    version = pw.IntegerField()

    class Meta:
        indexes = ((('address', 'uri'), True),)
        constraints = [pw.Check("version = 4 or version = 6")]

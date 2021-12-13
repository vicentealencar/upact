import peewee as pw

from datetime import datetime

from upact.models.base_model import BaseModel
from upact.models.uri import Uri

class BlockedIp(BaseModel):
    address = pw.CharField()
    uri = pw.ForeignKeyField(Uri, backref='ips', null=True)
    version = pw.IntegerField()
    created_at = pw.DateTimeField(default=datetime.now)
    updated_at = pw.DateTimeField(default=datetime.now)

    class Meta:
        indexes = ((('address', 'uri'), True),)
        constraints = [pw.Check("version = 4 or version = 6")]

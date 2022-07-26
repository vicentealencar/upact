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

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.address == other.address

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.address)

    class Meta:
        indexes = ((('address', 'uri'), True),)
        constraints = [pw.Check("version = 4 or version = 6")]

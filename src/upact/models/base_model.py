import peewee as pw
import playhouse.signals as ps

database_proxy = pw.DatabaseProxy()

class BaseModel(ps.Model):
    class Meta:
        database = database_proxy

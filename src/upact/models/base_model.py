import peewee as pw

database_proxy = pw.DatabaseProxy()

class BaseModel(pw.Model):
    class Meta:
        database = database_proxy

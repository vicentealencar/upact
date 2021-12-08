import peewee as pw
from datetime import datetime
from upact.models.base_model import BaseModel

class Uri(BaseModel):
    name = pw.CharField(default="")
    type_uri = pw.CharField(default="url", null=False)

    def is_active(self, when=datetime.now(), now_date=datetime.now()):
        return any([playtime.is_active(when=when, now_date=now_date) for playtime in self.playtime_rules])

    class Meta:
        constraints = [pw.Check("type_uri = 'url' or type_uri='application'")]

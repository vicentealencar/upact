import peewee as pw
from datetime import datetime
from upact.models.base_model import BaseModel

TYPE_URL = "url"
TYPE_APP = "application"
TYPE_PERMANENTLY_BLOCKED_IP = "permanently_blocked_ip"

class Uri(BaseModel):
    TYPE_URL = TYPE_URL
    TYPE_APP = TYPE_APP
    TYPE_PERMANENTLY_BLOCKED_IP = TYPE_PERMANENTLY_BLOCKED_IP

    name = pw.CharField(default="")
    type_uri = pw.CharField(default="url", null=False)

    def is_active(self, when=datetime.now(), now_date=datetime.now()):
        return any([playtime.is_active(when=when, now_date=now_date) for playtime in self.playtime_rules])

    class Meta:
        constraints = [pw.Check(f"type_uri='{TYPE_URL}' or type_uri='{TYPE_APP}' or type_uri='{TYPE_PERMANENTLY_BLOCKED_IP}'")]

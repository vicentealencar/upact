import peewee as pw
from upact.models.base_model import BaseModel

class Uri(BaseModel):
    name = pw.CharField(default="")
    type_uri = pw.CharField(default="url", null=False)

    class Meta:
        constraints = [pw.Check("type_uri = 'url' or type_uri='application'")]

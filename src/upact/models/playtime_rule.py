import peewee as pw
import playhouse.signals as ps

from datetime import datetime
from dateutil import rrule
from dateutil.parser import parse
from recurrent import RecurringEvent

from upact.models.base_model import BaseModel
from upact.models.uri import Uri

class PlaytimeRule(BaseModel):
    from_time = pw.TimeField()
    to_time = pw.TimeField()
    frequency = pw.CharField()
    uri = pw.ForeignKeyField(Uri, backref='playtime_rules')

    def is_active(self, when=None, now_date=datetime.now()):
        when = when or now_date
        recurrence_rule = rrule.rrulestr(RecurringEvent(now_date=now_date).parse(self.frequency), dtstart=now_date)

        day_in_recurrence = (recurrence_rule[0].date() - when.date()).days == 0
        time_in_interval = self.from_time <= when.time() and when.time() < self.to_time       

        return day_in_recurrence and time_in_interval

@ps.pre_save(sender=PlaytimeRule)
def verify_frequency_string(model_class, instance, created):
    if RecurringEvent().parse(instance.frequency) is None:
        raise ValueError(f"Invalid frequency: {instance.frequency}")


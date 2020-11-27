import json

class BlockedSites:
    def __init__(self, urls, playtime_days, playtime_hours, json_serializer=json.dumps, json_deserializer=json.loads):
        self.urls = urls
        self.playtime_days = playtime_days
        self.playtime_hours = playtime_hours
        self.json_serializer = json_serializer
        self.json_deserializer = json_deserializer

    def to_dict(self):
        return { 'urls': urls, 'playtime': { 'days': playtime_days, 'hours': playtime_hours } }

    def to_json(self):
        return self.json_serializer(self.to_dict())

    def serialize(self):
        return self.to_json()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError("Can't compare %s and %s" % (other.__class__.__name__, self.__class__.__name__))
        else:
            return self.urls == other.urls and self.playtime_days == other.playtime_days and\
                   self.playtime_hours == other.playtime_hours

    @staticmethod
    def deserialize(raw_str):
        deserialized = self.json_deserializer(raw_str)
        playtime = (deserialized.get('playtime') or {})
        return BlockedSites(deserialized['urls'], playtime.get('days'), playtime.get('hours'))

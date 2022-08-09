from upact.models import Uri, PlaytimeRule

def list(type_uri=None):

    if type_uri:
        return Uri.select().where(Uri.type_uri == type_uri)
    else:
        return Uri.select()


def block(urls_to_block, playtime_days=None, playtime_hours=[], type_uri=Uri.TYPE_URL):

    saved_uris = []
    for name in urls_to_block:
        uri = Uri(name=name, type_uri=type_uri)
        uri.save()

        for ph in (playtime_hours or []):
            playtime_rule = PlaytimeRule(from_time=ph[0], to_time=ph[1], frequency=playtime_days, uri=uri)
            playtime_rule.save()

        saved_uris.append(uri)

    return saved_uris

def remove(urls_to_remove):
    for name in urls_to_remove:
        for uri in Uri.select().where(Uri.name==name):
            uri.delete_instance(recursive=True, delete_nullable=True)


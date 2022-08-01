from upact.models import Uri, PlaytimeRule

def list(uri_type=None):

    if uri_type:
        return Uri.select().where(Uri.type_uri == uri_type)
    else:
        return Uri.select()


def block(names_list, playtime_days, playtime_hours):

    saved_uris = []
    for name in names_list:
        uri = Uri(name=name, type_uri=Uri.TYPE_URL)
        uri.save()

        for ph in playtime_hours:
            playtime_rule = PlaytimeRules(from_time=ph[0], to_time=ph[1], frequency=playtime_days, uri=uri)
            playtime_rule.save()

        saved_uris.append(uri)

    return saved_uris

def remove(names_list):
    for name in urls_to_remove:
        Uri.select().find_one(Uri.name==name).delete_instance(recursive=True)

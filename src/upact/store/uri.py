from upact.models.uri import Uri

def list(uri_type=None):

    if uri_type:
        return Uri.select().where(Uri.type_uri == uri_type)
    else:
        return Uri.select()


def remove(names_list):
    for name in urls_to_remove:
        Uri.select().find_one(Uri.name==name).delete_instance(recursive=True)

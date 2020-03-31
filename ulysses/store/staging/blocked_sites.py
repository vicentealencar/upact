import ulysses.config as config

from ulysses.models import BlockedSites
from ulysses.store.file import GenericStore

class BlockedSites(GenericStore):
    def __init__(self, filename=config.STAGING_URLS_TO_BLOCK, deserialize=BlockedSites.deserialize, open_func=open):
        super().__init__(filename, deserialize, open_func)

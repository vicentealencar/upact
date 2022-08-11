import logging

import peewee as pw

from upact.models import database_proxy

import upact.fences.web as web_fence

class BasePlatform(object):
    def __init__(self, config):
        self.config = config

    def update_permanently_blocked_ips(self, ips_to_block):
        raise NotImplementedError()

    def update_ips_from_urls(self, ips_to_block, ips_to_unblock):
        raise NotImplementedError()

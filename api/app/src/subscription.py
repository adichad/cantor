import logging
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Subscription(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "subscription", id)

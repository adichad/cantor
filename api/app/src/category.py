import logging
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Category(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "category", id)




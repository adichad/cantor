import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB
logger = logging.getLogger()


class Unit(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "unit", id)
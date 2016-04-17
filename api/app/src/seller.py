import uuid
import binascii
import logging
import itertools
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Seller(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "seller", id)

    
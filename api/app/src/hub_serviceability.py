import uuid
import binascii
import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog
from variant import Variant

logger = logging.getLogger()


class HubServiceability(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "hub_serviceability", id)

